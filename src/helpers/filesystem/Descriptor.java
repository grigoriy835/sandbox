package helpers.filesystem;

import helpers.annotation.ItsShit;
import org.jetbrains.annotations.Contract;

import java.util.HashMap;

public class Descriptor {

    private static HashMap<String, Descriptor> descriptors = new HashMap<String, Descriptor>();

    @ItsShit(trueShit = false)
    public static Descriptor getDescriptor(String path) {
        String formattedPath = Descriptor.modifyPath(path);

        Descriptor.descriptors.put(formattedPath, new Descriptor());
        return Descriptor.descriptors.get(formattedPath);
    }

    @Contract(value = "_ -> param1", pure = true)
    protected static String modifyPath(String path){
        return String.format("1");
    }
}
