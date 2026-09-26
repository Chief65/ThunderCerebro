using System;
using System.IO;
using System.Text.RegularExpressions;

class Program {
    static void Main(string[] args) {
        string dir = @"creator/lab";
        for (int i = 1; i <= 5; i++) {
            string file = i == 1 ? "vialdealmas.yml" : $"vialdealmas_{i}.yml";
            string path = Path.Combine(dir, file);
            string content = File.ReadAllText(path);
            
            // Reemplazar la seccion de sonidos de liberacion
            // Patron actual: execute at %player% run playsound minecraft:entity.zombie.break_wooden_door master %player% ~ ~ ~ 0.9 1.1 +++ execute at %player% run playsound minecraft:block.amethyst_cluster.hit master %player% ~ ~ ~ 1.1 2.0
            // Nuevo: agregamos +++ execute at %player% run playsound minecraft:entity.vex.death master %player% ~ ~ ~ 0.85 1.25
            
            string target = "execute at %player% run playsound minecraft:entity.zombie.break_wooden_door master %player% ~ ~ ~ 0.9 1.1 +++ execute at %player% run playsound minecraft:block.amethyst_cluster.hit master %player% ~ ~ ~ 1.1 2.0";
            string replacement = target + " +++ execute at %player% run playsound minecraft:entity.vex.death master %player% ~ ~ ~ 0.85 1.25";
            
            if (content.Contains(target)) {
                content = content.Replace(target, replacement);
                File.WriteAllText(path, content, System.Text.Encoding.UTF8);
                Console.WriteLine($"Actualizado con exito: {file}");
            } else {
                Console.WriteLine($"No encontrado target en: {file}");
            }
        }
    }
}
