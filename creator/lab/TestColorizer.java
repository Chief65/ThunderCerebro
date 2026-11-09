import su.nightexpress.nightcore.util.Colorizer;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.serializer.legacy.LegacyComponentSerializer;

public class TestColorizer {
    public static void main(String[] args) {
        String[] samples = new String[]{
            "<#A335EE>Casco Bastión",
            "&6&l[MÍTICA] &fEspada",
            "<gradient:#a335ee:#ff007f>Caja Mítica</gradient>",
            "&d&l[&f&lMÍTICA&d&l] <#00ff7f>Armadura Pro"
        };
        for (String s : samples) {
            String applied = Colorizer.apply(s);
            Component comp = LegacyComponentSerializer.legacySection().deserialize(applied);
            System.out.println("Original: " + s);
            System.out.println("  Applied: " + applied.replace("§", "&"));
            System.out.println("  Comp: " + comp);
        }
    }
}
