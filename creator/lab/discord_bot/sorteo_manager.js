import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DB_PATH = path.join(__dirname, 'sorteos_db.json');

// Inicializar base de datos local en JSON
function getDB() {
  if (!fs.existsSync(DB_PATH)) {
    fs.writeFileSync(DB_PATH, JSON.stringify({ active: {}, finished: {} }, null, 2), 'utf8');
  }
  return JSON.parse(fs.readFileSync(DB_PATH, 'utf8'));
}

function saveDB(data) {
  fs.writeFileSync(DB_PATH, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * Genera el payload del embed oficial de sorteo de ThunderMC
 */
export function buildGiveawayPayload({
  messageId = null,
  title = "🎉 ¡Sorteo Oficial de ThunderMC!",
  prize = "🏆 Rango Titán [Permanente]",
  entriesCount = 0,
  endTimestamp = Math.floor(Date.now() / 1000) + 172800, // 48h default
  winnersCount = 3,
  isFinished = false,
  winners = []
}) {
  const statusLine = isFinished
    ? `**Estado del Sorteo:**\n# 🏁 \`FINALIZADO\`\n\`👑\` **Ganadores:** ${winners.length > 0 ? winners.map(w => `<@${w}>`).join(', ') : 'Sin participantes suficientes'}`
    : `**Estado del Sorteo:**\n# ⏳ <t:${endTimestamp}:R>\n\`📅\` Finaliza: <t:${endTimestamp}:F>\n\`👑\` Ganadores: \`${winnersCount} afortunados\`\n\`🎟️\` Entradas registradas: \`${entriesCount} participantes\``;

  return {
    allowed_mentions: { parse: ["everyone", "users"] },
    embeds: [
      {
        title,
        description: `¡Participa gratis y llévate increíbles recompensas para tu aventura!\n-# ꜱᴏʀᴛᴇᴏ ᴇxᴄʟᴜꜱɪᴠᴏ ᴘᴀʀᴀ ᴛᴏᴅᴀ ʟᴀ ᴄᴏᴍᴜɴɪᴅᴀᴅ ᴅᴇ ᴛʜᴜɴᴅᴇʀᴍᴄ\n\n**Premio del Sorteo:**\n# ${prize.startsWith('🏆') ? prize : `🏆 \`${prize}\``}\n\n${statusLine}\n\n## ¿Cómo Participar?\n${isFinished ? 'El sorteo ha concluido.' : 'Haz clic en el botón verde inferior para registrar tu entrada al instante.'}\n\n-# [Tienda](https://tienda.thundermc.es/) • [Tiktok](https://www.tiktok.com/@somosthundermc_?lang=es) • [YouTube](https://www.youtube.com/@somosthundermc/featured)`,
        color: isFinished ? 9807270 : 16706304,
        thumbnail: {
          url: "https://cdn.discordapp.com/attachments/1557075345906081792/1557218262607986769/purple_bundle_closed.png?backend=b2&ex=6ac70005&is=6ac5ae85&hm=68a1a7521ba0d379bfb0b9c76e7275c3a53238b255ad5e50e131ba227b649426&"
        }
      }
    ],
    components: [
      {
        type: 1,
        components: [
          {
            type: 2,
            style: 3,
            custom_id: "sorteo_participar",
            label: isFinished ? "Sorteo Finalizado" : "¡Participar en el Sorteo!",
            emoji: { name: "🎉" },
            disabled: isFinished
          }
        ]
      }
    ]
  };
}

/**
 * Procesa la interacción de un botón en Discord
 */
export async function handleGiveawayInteraction(interaction, discordToken) {
  const { custom_id } = interaction.data;
  const userId = interaction.member?.user?.id || interaction.user?.id;
  const username = interaction.member?.user?.username || interaction.user?.username;
  const messageId = interaction.message.id;

  const db = getDB();
  const giveaway = db.active[messageId] || {
    id: messageId,
    endTimestamp: Math.floor(Date.now() / 1000) + 172800,
    entries: []
  };

  if (custom_id === "sorteo_participar") {
    const alreadyIn = giveaway.entries.some(e => e.userId === userId);

    if (alreadyIn) {
      // Respuesta efímera informando que ya está registrado
      return {
        type: 4, // CHANNEL_MESSAGE_WITH_SOURCE
        data: {
          flags: 64, // EPHEMERAL
          content: `⚠️ **¡Ya estás participando, ${username}!**\nTu entrada ya está registrada en el sistema. Mucha suerte en el sorteo.`
        }
      };
    }

    // Registrar entrada
    giveaway.entries.push({ userId, username, joinedAt: Date.now() });
    db.active[messageId] = giveaway;
    saveDB(db);

    // Actualizar el embed original con el nuevo conteo de entradas
    const updatedPayload = buildGiveawayPayload({
      entriesCount: giveaway.entries.length,
      endTimestamp: giveaway.endTimestamp
    });

    // Enviar actualizacion del mensaje (type 7: UPDATE_MESSAGE)
    return {
      type: 7,
      data: updatedPayload
    };
  }

  if (custom_id === "sorteo_ver_estado") {
    const entry = giveaway.entries.find(e => e.userId === userId);
    const content = entry
      ? `✅ **Estado:** Participando activamente con **1 entrada**.\n📅 Registrado: <t:${Math.floor(entry.joinedAt / 1000)}:R>`
      : `❌ **Estado:** Aún no te has registrado en este sorteo. Pulsa el botón verde para entrar.`;

    return {
      type: 4,
      data: {
        flags: 64, // EPHEMERAL
        content
      }
    };
  }

  return null;
}
