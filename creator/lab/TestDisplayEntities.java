import org.bukkit.Location;
import org.bukkit.Material;
import org.bukkit.World;
import org.bukkit.entity.BlockDisplay;
import org.bukkit.entity.Display;
import org.bukkit.entity.ItemDisplay;
import org.bukkit.entity.TextDisplay;
import org.bukkit.util.Transformation;
import org.joml.Vector3f;
import org.joml.Quaternionf;

public class TestDisplayEntities {
    public static void test(World world, Location loc) {
        BlockDisplay bd = world.spawn(loc, BlockDisplay.class);
        bd.setBlock(Material.PURPLE_SHULKER_BOX.createBlockData());
        Transformation t = new Transformation(
            new Vector3f(-0.5f, 0.0f, -0.5f),
            new Quaternionf(),
            new Vector3f(1.0f, 0.5f, 1.0f),
            new Quaternionf()
        );
        bd.setTransformation(t);
        bd.setInterpolationDelay(0);
        bd.setInterpolationDuration(15);

        ItemDisplay id = world.spawn(loc, ItemDisplay.class);
        id.setBillboard(Display.Billboard.CENTER);

        TextDisplay td = world.spawn(loc, TextDisplay.class);
        td.setBillboard(Display.Billboard.CENTER);
    }
}
