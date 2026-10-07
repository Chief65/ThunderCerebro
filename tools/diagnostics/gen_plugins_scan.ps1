$pluginDirs = @(
    "plugins/ItemEdit", "plugins/Jobs", "plugins/JustRTP", "plugins/LibsDisguises", 
    "plugins/LiteBans", "plugins/LootChests", "plugins/LuckPerms", "plugins/MMOItems", 
    "plugins/Multiverse-Core", "plugins/MythicLib", "plugins/MythicMobs", "plugins/NBTAPI", 
    "plugins/PlaceholderAPI", "plugins/Plan", "plugins/PlayerKits2", "plugins/PlayerPoints", 
    "plugins/PlayerWarps", "plugins/ProtectionMenu", "plugins/ProtectionStones", "plugins/PvPManager", 
    "plugins/QuickShop-Hikari", "plugins/RankUp", "plugins/RoseGarden", "plugins/SCore", 
    "plugins/ShopGUIPlus", "plugins/ShopGUIPlus-SellGUI", "plugins/Shopkeepers", "plugins/SilkSpawners_v2", 
    "plugins/SkinsRestorer", "plugins/TAB", "plugins/Tebex", "plugins/ThunderCurrencys", 
    "plugins/ThunderMines", "plugins/Topper", "plugins/UltimateKoth", "plugins/ValyrTutorial", 
    "plugins/Vault", "plugins/ViaVersion", "plugins/VoidGen", "plugins/VoidSpawn", 
    "plugins/WorldGuard", "plugins/ZelAuction", "plugins/ZelChat", "plugins/ZelTeams", 
    "plugins/bStats", "plugins/cAFKZone", "plugins/faststats", "plugins/floodgate", 
    "plugins/nightcore", "plugins/spark", "plugins/voicechat"
)

$sb = [System.Text.StringBuilder]::new()
foreach ($d in $pluginDirs) {
    [void]$sb.AppendLine("ls -lh $d")
}
[void]$sb.AppendLine("bye")
[System.IO.File]::WriteAllText("C:\Users\PC\Desktop\ThunderCerebro\sftp_all_plugins.txt", $sb.ToString())
Write-Output "Generated sftp_all_plugins.txt with $($pluginDirs.Count) plugins"
