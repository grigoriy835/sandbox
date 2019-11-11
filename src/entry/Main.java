package entry;

import helpers.filesystem.Descriptor;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.lang.StringBuilder;
import java.util.Arrays;

public class Main {

    public static void mai(String[] args) {

    }

    public static void main(String[] args) {

    }

    public static void main2(String[] args) {
        // toCamelCase function----------------------------------------------------------------------------
        String s = "qwe_rty-uio_asd-fgh-zxc_vbn";
        String[] substring;
        if (s.indexOf('_') >= 0) {
            substring = s.split("_");
        } else {
            substring = s.split("-");
        }

        String tt = substring[0];
        for (int i = 1; i < substring.length; i++) {
            tt = tt.concat(new String(new char[]{ java.lang.Character.toUpperCase(substring[i].charAt(0))}));
            tt = tt.concat(substring[i].substring(1));
        }

        // toCamelCase function--------------------------------------------------------------------------------
        Matcher m = Pattern.compile("[_|-](\\w)").matcher(s);
        StringBuffer sb = new StringBuffer();
        while (m.find()) {
            m.appendReplacement(sb, m.group(1).toUpperCase());
        }
        tt = m.appendTail(sb).toString();

        // toCamelCase function------------------------------------------------------------------
        String[] words = s.split("[-_]");
        tt = Arrays.stream(words, 1, words.length)
                .map(str -> str.substring(0, 1).toUpperCase() + str.substring(1))
                .reduce(words[0], String::concat);
    }

    public static void main1(String[] args) {
        System.out.println("Hi bitch");

        Descriptor someDescriptor = Descriptor.getDescriptor("/example");
    }
}
