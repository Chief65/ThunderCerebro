import subprocess, glob

java_code = """import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.minimessage.MiniMessage;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;

public class TestMiniMessage {
    public static Component parse(String input) {
        if (input == null || input.isBlank()) return Component.empty();
        
        // If it already has MiniMessage tags (<...>):
        if (input.contains("<") && input.contains(">")) {
            try {
                // If it ALSO has legacy & codes, convert legacy codes first:
                String formatted = input;
                if (formatted.contains("&") || formatted.contains("§")) {
                    formatted = formatted.replace("§", "&")
                        .replace("&0", "<black>").replace("&1", "<dark_blue>").replace("&2", "<dark_green>")
                        .replace("&3", "<dark_aqua>").replace("&4", "<dark_red>").replace("&5", "<dark_purple>")
                        .replace("&6", "<gold>").replace("&7", "<gray>").replace("&8", "<dark_gray>")
                        .replace("&9", "<blue>").replace("&a", "<green>").replace("&b", "<aqua>")
                        .replace("&c", "<red>").replace("&d", "<light_purple>").replace("&e", "<yellow>")
                        .replace("&f", "<white>").replace("&l", "<bold>").replace("&o", "<italic>")
                        .replace("&n", "<underlined>").replace("&m", "<strikethrough>").replace("&r", "<reset>");
                }
                return MiniMessage.miniMessage().deserialize(formatted);
            } catch (Exception ignored) {}
        }
        
        // Otherwise use LegacyComponentSerializer:
        return LegacyComponentSerializer.legacyAmpersand().deserialize(input.replace('§', '&'));
    }

    public static void main(String[] args) {
        String s1 = "<#A335EE>Casco Bastión";
        String s2 = "&6&l[MÍTICA] &fEspada";
        String s3 = "<gradient:#a335ee:#ff007f>Caja Mítica</gradient>";
        String s4 = "&d&l[&f&lMÍTICA&d&l] <#00ff7f>Armadura Pro";

        System.out.println("s1 parsed: " + parse(s1));
        System.out.println("s2 parsed: " + parse(s2));
        System.out.println("s3 parsed: " + parse(s3));
        System.out.println("s4 parsed: " + parse(s4));
    }
}
"""

with open("creator/lab/TestMiniMessage.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/TestMiniMessage.java"], capture_output=True, text=True)
if res.returncode != 0:
    print("javac error:", res.stderr)
else:
    res2 = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "TestMiniMessage"], capture_output=True, text=True)
    print(res2.stdout)
