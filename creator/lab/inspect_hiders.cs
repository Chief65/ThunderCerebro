using System;
using System.IO;
using System.Text.RegularExpressions;

class Program {
    static void Main() {
        byte[] bytes = File.ReadAllBytes("creator/lab/Hiders.class");
        string text = System.Text.Encoding.ASCII.GetString(bytes);
        foreach (Match m in Regex.Matches(text, "[A-Za-z0-9_]{3,}")) {
            if (m.Value.IndexOf("hide", StringComparison.OrdinalIgnoreCase) >= 0 ||
                m.Value.IndexOf("potion", StringComparison.OrdinalIgnoreCase) >= 0 ||
                m.Value.IndexOf("tooltip", StringComparison.OrdinalIgnoreCase) >= 0) {
                Console.WriteLine(m.Value);
            }
        }
    }
}
