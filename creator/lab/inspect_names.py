import subprocess, glob

java_code = """import su.nightexpress.excellentcrates.CratesPlugin;
import su.nightexpress.excellentcrates.crate.impl.Crate;
import su.nightexpress.excellentcrates.api.crate.Reward;
import su.nightexpress.nightcore.config.FileConfig;
import su.nightexpress.nightcore.util.Colorizer;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;

import java.io.File;

public class InspectRewardNames {
    public static void main(String[] args) {
        File file = new File("creator/lab/mitica.yml");
        FileConfig config = new FileConfig(file);
        config.load();

        System.out.println("Config loaded: " + config.getFile().getName());
        for (String key : config.getSection("Rewards.List")) {
            System.out.println("=== Reward Key: " + key + " ===");
            String rawItem = config.getString("Rewards.List." + key + ".PreviewData.Data.Value", "");
            if (rawItem.contains("custom_name")) {
                int start = rawItem.indexOf("custom_name");
                System.out.println("custom_name snippet: " + rawItem.substring(start, Math.min(rawItem.length(), start + 250)));
            }
        }
    }
}
"""

with open("creator/lab/InspectRewardNames.java", "w", encoding="utf-8") as f:
    f.write(java_code)

cp = ";".join(glob.glob("creator/lib/*.jar"))
res = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\javac.exe", "-proc:none", "-cp", cp, "creator/lab/InspectRewardNames.java"], capture_output=True, text=True)
if res.returncode != 0:
    print("javac error:", res.stderr)
else:
    res2 = subprocess.run([r"C:\Program Files\Java\jdk-21\bin\java.exe", "-cp", "creator/lab;" + cp, "InspectRewardNames"], capture_output=True, text=True)
    print(res2.stdout)
    print(res2.stderr)
