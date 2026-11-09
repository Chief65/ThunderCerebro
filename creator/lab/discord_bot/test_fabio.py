"""Pruebas sin conexión a Discord: python -m unittest -v test_fabio.py"""
from __future__ import annotations

import asyncio
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import gateway_bot as b


class FakeInteraction:
    def __init__(self, *, custom_id="", user_id="123", interaction_id="456", values=None):
        self.id = interaction_id
        self.user_id = user_id
        self.user_name = "Candidato"
        self.guild_id = b.GUILD_ID
        self.channel_id = b.ADMIN_CHANNEL_ID
        self.member = {"permissions": str(b.PERM_ADMINISTRATOR), "roles": []}
        self.custom_id = custom_id
        self.application_id = b.APP_ID
        self.message = {}
        self._values = values or {}
        self.defer = AsyncMock()
        self.defer_update = AsyncMock()
        self.reply = AsyncMock()
        self.edit_original = AsyncMock()
        self.followup = AsyncMock()
        self.open_modal = AsyncMock()
        self.update_message = AsyncMock()

    def modal_values(self):
        return self._values


class PureTests(unittest.TestCase):
    def test_json_configuration_works(self):
        for path in (*b.RULE_FILES.values(), b.FILE_SORTEO_CFG):
            self.assertIsInstance(json.loads(Path(path).read_text(encoding="utf-8")), dict)
        self.assertTrue(b._load_first_embed(b.RULE_FILES["reglas_generales"]))

    def test_admin_authorization_requires_real_permission(self):
        inter = FakeInteraction()
        inter.member["permissions"] = "0"
        with patch.object(b, "REVIEWER_ROLE_IDS", frozenset()):
            self.assertFalse(b._is_reviewer(inter))
            inter.member["permissions"] = str(b.PERM_ADMINISTRATOR)
            self.assertTrue(b._is_reviewer(inter))
        inter.member["permissions"] = "0"
        inter.member["roles"] = ["777"]
        with patch.object(b, "REVIEWER_ROLE_IDS", frozenset({"777"})):
            self.assertTrue(b._is_reviewer(inter))
            inter.guild_id = "other"
            self.assertFalse(b._is_reviewer(inter))

    def test_application_schema_never_drops_bad_data(self):
        db = {"counter": "100", "applications": {"TH-1": {"user_id": "42"}}}
        self.assertEqual(b._normalize_db(db)["counter"], 100)
        for value in ([{"id": "bad"}], "invalid", None):
            with self.subTest(value=value), self.assertRaises(b.StoreCorruptedError):
                b._normalize_db({"applications": value})
        with self.assertRaises(b.StoreCorruptedError):
            b._normalize_db({"counter": -2, "applications": {}})

    def test_raffle_schema_never_drops_bad_data(self):
        self.assertEqual(b._normalize_sorteos({})["entries"], [])
        for value in ({}, "wrong", [3]):
            with self.subTest(value=value), self.assertRaises(b.StoreCorruptedError):
                b._normalize_sorteos({"entries": value})

    def test_error_redacts_discord_webhook_tokens(self):
        cases = [
            "/interactions/123456/supersecreto/callback",
            "/webhooks/987654/supersecreto/messages/@original",
        ]
        for path in cases:
            message = str(b.DiscordAPIError("POST", path, 403, {"code": 50013, "message": "supersecreto"}))
            self.assertNotIn("supersecreto", message)
            self.assertIn("[redactado]", message)

    def test_role_automatic_assignment_disabled_by_default(self):
        with patch.object(b, "_setting", return_value=""), patch.object(b, "discord_request", new_callable=AsyncMock) as req:
            ok, info = asyncio.run(b.assign_category_role(b.CATEGORIES["postulacion_staff"], "123"))
            self.assertFalse(ok)
            self.assertIn("ROLE_ID_STAFF", info)
            req.assert_not_awaited()

    def test_role_fallback_filters_high_privileges(self):
        roles = [
            {"id": "77", "name": "staff", "permissions": str(1 << 28), "position": 0},
            {"id": "78", "name": "staff", "permissions": "0", "position": 1},
        ]
        self.assertEqual(b._match_role(roles, ("staff",))["id"], "78")

    def test_modal_components_extract_legacy_and_v2(self):
        raw = {
            "id": "123", "token": "hidden", "type": 5,
            "data": {"custom_id": "t", "components": [
                {"components": [{"custom_id": "a", "value": " si "}]},
                {"component": {"custom_id": "b", "value": " no "}},
            ]},
        }
        self.assertEqual(b.Interaction(raw).modal_values(), {"a": "si", "b": "no"})

    def test_routes_unchanged(self):
        for custom_id in ("select_postulacion_tipo", "sorteo_participar", "sorteo_ver_estado", "select_reglas_normativa"):
            self.assertIn((b.IType.COMPONENT, custom_id), b._EXACT_ROUTES)
        for cat in b.CATEGORIES.values():
            self.assertIn((b.IType.MODAL_SUBMIT, cat.modal_id), b._EXACT_ROUTES)


class StorageTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = str(Path(self.tmp.name) / "store.json")
        self.store = b.JsonStore(self.path, lambda: {"n": 0})

    async def asyncTearDown(self):
        self.tmp.cleanup()

    async def test_atomic_concurrent_transactions(self):
        async def increase():
            async with self.store.transaction() as data:
                old = data["n"]
                await asyncio.sleep(0)
                data["n"] = old + 1
        await asyncio.gather(*(increase() for _ in range(35)))
        self.assertEqual((await self.store.read())["n"], 35)
        self.assertEqual(json.loads(Path(self.path).read_text())["n"], 35)
        self.assertFalse(list(Path(self.tmp.name).glob("*.tmp")))

    async def test_rollback_does_not_modify_disk(self):
        async with self.store.transaction() as data:
            data["n"] = 1
        with self.assertRaises(RuntimeError):
            async with self.store.transaction() as data:
                data["n"] = 99
                raise RuntimeError("fallo")
        self.assertEqual((await self.store.read())["n"], 1)

    async def test_corrupt_file_stays_intact_and_backup_exists(self):
        Path(self.path).write_text("{esto no es json", encoding="utf8")
        with self.assertRaises(b.StoreCorruptedError):
            await self.store.read()
        self.assertEqual(Path(self.path).read_text(), "{esto no es json")
        self.assertEqual(len(list(Path(self.tmp.name).glob("store.json.corrupt-*"))), 1)


class HandlerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.posts = b.JsonStore(str(base / "postulaciones_db.json"), lambda: {"counter": 100, "applications": {}})
        self.raffles = b.JsonStore(str(base / "sorteos_db.json"), lambda: {"entries": []})
        self.patches = [
            patch.object(b, "STORE_POSTULACIONES", self.posts),
            patch.object(b, "STORE_SORTEOS", self.raffles),
        ]
        for item in self.patches:
            item.start()

    async def asyncTearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.tmp.cleanup()

    @staticmethod
    def staff_values():
        return {
            "field_nombre_real": "Persona Prueba", "field_nick_edad": "Steve 18",
            "field_pais": "España", "field_horas_exp": "Tengo experiencia como staff",
            "field_motivo": "Quiero colaborar con este equipo",
        }

    async def test_two_same_user_submissions_create_only_one(self):
        first = FakeInteraction(custom_id="modal_submit_staff", values=self.staff_values())
        second = FakeInteraction(custom_id="modal_submit_staff", values=self.staff_values())
        with patch.object(b, "send_dm", new_callable=AsyncMock, return_value={"id": "dm"}), \
             patch.object(b, "post_message", new_callable=AsyncMock, return_value={"id": "admin-1"}) as post:
            await asyncio.gather(b.on_submit_postulacion(first), b.on_submit_postulacion(second))
        data = await self.posts.read()
        self.assertEqual(list(data["applications"]), ["TH-101"])
        self.assertEqual(post.await_count, 1)
        self.assertEqual(first.defer.await_count + second.defer.await_count, 2)
        self.assertEqual(first.edit_original.await_count + second.edit_original.await_count, 2)

    async def test_submission_validates_min_lengths(self):
        values = self.staff_values()
        values["field_nombre_real"] = "A"
        inter = FakeInteraction(custom_id="modal_submit_staff", values=values)
        await b.on_submit_postulacion(inter)
        inter.reply.assert_awaited_once()
        self.assertFalse((await self.posts.read())["applications"])

    async def test_accept_rolls_back_after_failed_dm(self):
        await self.insert_app(status=b.Status.PENDING)
        inter = FakeInteraction(custom_id="admin_accept_TH-101")
        with patch.object(b, "send_dm", new_callable=AsyncMock, return_value=None), \
             patch.object(b, "refresh_admin_current", new_callable=AsyncMock):
            await b.on_admin_accept(inter)
        app = (await self.posts.read())["applications"]["TH-101"]
        self.assertEqual(app["status"], b.Status.PENDING)
        inter.defer_update.assert_awaited_once()
        inter.followup.assert_awaited_once()

    async def test_signing_twice_does_not_duplicate_invite_or_role(self):
        await self.insert_app(status=b.Status.CONTRACT_SENT)
        first = FakeInteraction(custom_id="user_sign_contract_TH-101")
        second = FakeInteraction(custom_id="user_sign_contract_TH-101")
        with patch.object(b, "assign_category_role", new_callable=AsyncMock, return_value=(True, "Staff")) as role, \
             patch.object(b, "create_single_use_invite", new_callable=AsyncMock, return_value="https://discord.gg/test") as invite, \
             patch.object(b, "refresh_admin_current", new_callable=AsyncMock), \
             patch.object(b, "notify_admins", new_callable=AsyncMock, return_value=True) as notice:
            await asyncio.gather(b.on_sign_contract(first), b.on_sign_contract(second))
        app = (await self.posts.read())["applications"]["TH-101"]
        self.assertEqual(app["status"], b.Status.SIGNED)
        self.assertTrue(app["welcome_delivered"])
        self.assertTrue(app["role_assigned"])
        self.assertEqual(app["onboarding_invite_url"], "https://discord.gg/test")
        role.assert_awaited_once()
        invite.assert_awaited_once()
        notice.assert_awaited_once()
        self.assertEqual(first.edit_original.await_count + second.edit_original.await_count, 1)

    async def test_signing_retry_reuses_invite_when_dm_edit_failed(self):
        await self.insert_app(status=b.Status.CONTRACT_SENT)
        first = FakeInteraction(custom_id="user_sign_contract_TH-101")
        first.edit_original.side_effect = b.DiscordAPIError(
            "PATCH", "/webhooks/123/secret/messages/@original", 403, {"code": 50013}
        )
        second = FakeInteraction(custom_id="user_sign_contract_TH-101")
        with patch.object(b, "assign_category_role", new_callable=AsyncMock, return_value=(True, "Staff")) as role, \
             patch.object(b, "create_single_use_invite", new_callable=AsyncMock, return_value="https://discord.gg/test") as invite, \
             patch.object(b, "send_dm", new_callable=AsyncMock, return_value=None), \
             patch.object(b, "refresh_admin_current", new_callable=AsyncMock), \
             patch.object(b, "notify_admins", new_callable=AsyncMock, return_value=True):
            await b.on_sign_contract(first)
            before = (await self.posts.read())["applications"]["TH-101"]
            self.assertFalse(before["welcome_delivered"])
            await b.on_sign_contract(second)
        after = (await self.posts.read())["applications"]["TH-101"]
        self.assertTrue(after["welcome_delivered"])
        role.assert_awaited_once()
        invite.assert_awaited_once()

    async def test_sorteo_double_click_and_counter_reads_latest_message(self):
        one = FakeInteraction(custom_id="sorteo_participar")
        two = FakeInteraction(custom_id="sorteo_participar")
        original = {"id": "777", "author": {"id": b.APP_ID}, "embeds": [{
            "description": "Participantes: `0 participantes` (antiguo)"}]}
        latest = {"id": "777", "author": {"id": b.APP_ID}, "embeds": [{
            "description": "Participantes: `0 participantes` (mensaje NUEVO)", "title": "Actualizado"}]}
        one.message = original
        two.message = original
        with patch.object(b, "discord_request", new_callable=AsyncMock, return_value=latest) as get, \
             patch.object(b, "edit_message", new_callable=AsyncMock) as edit:
            await asyncio.gather(b.on_sorteo_participar(one), b.on_sorteo_participar(two))
        self.assertEqual(len((await self.raffles.read())["entries"]), 1)
        get.assert_awaited_once()
        self.assertIn("mensaje NUEVO", edit.await_args.args[2]["embeds"][0]["description"])
        self.assertIn("1 participantes", edit.await_args.args[2]["embeds"][0]["description"])
        self.assertEqual(one.edit_original.await_count + two.edit_original.await_count, 2)

    async def test_retry_after_nan_does_not_raise(self):
        replies = [(429, {"retry_after": float("nan")}, {}), (200, {"ok": True}, {})]
        with patch.object(b, "_http_request", side_effect=replies), \
             patch.object(b.asyncio, "sleep", new_callable=AsyncMock) as sleep:
            result = await b.discord_request("GET", "/test")
        self.assertEqual(result, {"ok": True})
        sleep.assert_awaited_once()

    async def test_reject_reason_ack_and_audit(self):
        await self.insert_app(status=b.Status.PENDING)
        inter = FakeInteraction(custom_id="modal_reason_reject_TH-101", values={
            "field_reject_reason": "Falta experiencia para este puesto."
        })
        with patch.object(b, "send_dm", new_callable=AsyncMock, return_value={"id": "dm"}), \
             patch.object(b, "refresh_admin_current", new_callable=AsyncMock), \
             patch.object(b, "notify_admins", new_callable=AsyncMock, return_value=True):
            await b.on_reject_reason(inter)
        record = (await self.posts.read())["applications"]["TH-101"]
        self.assertEqual(record["status"], b.Status.REJECTED)
        inter.defer.assert_awaited_once()
        inter.edit_original.assert_awaited_once()
        inter.reply.assert_not_awaited()

    async def test_reject_reason_race_does_not_override_contract(self):
        await self.insert_app(status=b.Status.CONTRACT_SENT)
        inter = FakeInteraction(custom_id="modal_reason_reject_TH-101", values={
            "field_reject_reason": "Explicación suficientemente larga"
        })
        await b.on_reject_reason(inter)
        self.assertEqual((await self.posts.read())["applications"]["TH-101"]["status"], b.Status.CONTRACT_SENT)
        inter.defer.assert_awaited_once()
        self.assertIn("procesada", inter.edit_original.await_args.args[0]["content"])

    async def test_decline_early_ack_with_dm_edit_fallback(self):
        await self.insert_app(status=b.Status.CONTRACT_SENT)
        inter = FakeInteraction(custom_id="user_decline_contract_TH-101")
        inter.edit_original.side_effect = b.DiscordAPIError(
            "PATCH", "/webhooks/123/secret/messages/@original", 403, {"code": 50013}
        )
        with patch.object(b, "refresh_admin_current", new_callable=AsyncMock), \
             patch.object(b, "notify_admins", new_callable=AsyncMock, return_value=True), \
             patch.object(b, "edit_message", new_callable=AsyncMock) as edit:
            await b.on_decline_contract(inter)
        self.assertEqual((await self.posts.read())["applications"]["TH-101"]["status"], b.Status.DECLINED)
        inter.defer_update.assert_awaited_once()
        # An old application without DM identifiers cannot be edited by channel.
        edit.assert_not_awaited()
        inter.followup.assert_awaited_once()

    async def test_wrong_signer_only_receives_followup(self):
        await self.insert_app(status=b.Status.CONTRACT_SENT)
        inter = FakeInteraction(custom_id="user_sign_contract_TH-101", user_id="999")
        await b.on_sign_contract(inter)
        inter.defer_update.assert_awaited_once()
        inter.followup.assert_awaited_once()
        inter.reply.assert_not_awaited()
        self.assertEqual((await self.posts.read())["applications"]["TH-101"]["status"], b.Status.CONTRACT_SENT)

    async def test_sorteo_status_with_legacy_invalid_timestamp(self):
        async with self.raffles.transaction() as data:
            data["entries"] = [{"userId": "123", "joinedAt": "fecha-inválida"}]
        inter = FakeInteraction(custom_id="sorteo_ver_estado")
        await b.on_sorteo_estado(inter)
        inter.defer.assert_awaited_once()
        self.assertIn("participando", inter.edit_original.await_args.args[0]["content"])

    async def test_callback_rate_limit_fails_fast(self):
        with patch.object(b, "_http_request", return_value=(429, {"retry_after": 40}, {})), \
             patch.object(b.asyncio, "sleep", new_callable=AsyncMock) as sleep:
            with self.assertRaises(b.DiscordAPIError):
                await b.discord_request("POST", "/interactions/123/secret/callback", {"type": 4}, auth=False)
        sleep.assert_not_awaited()

    async def insert_app(self, *, status):
        async with self.posts.transaction() as db:
            db["applications"]["TH-101"] = {
                "id": "TH-101", "user_id": "123", "username": "Test",
                "categoria": "postulacion_staff", "tipo": "Staff / Moderación",
                "submitted_at": 1700000000, "status": status,
                "resumen_fields": [], "admin_msg_id": "55",
            }


if __name__ == "__main__":
    unittest.main()
