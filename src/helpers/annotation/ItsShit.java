package helpers.annotation;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

// Сначала укажем, что аннотацию надо применять на уровне ПОЛЯ
@Target(ElementType.METHOD)
// Использовать аннотацию надо во время выполнения программы
@Retention(RetentionPolicy.RUNTIME)

public @interface ItsShit {
    // Выбираем, сравнивать ли источники. По умолчанию — да.
    boolean trueShit() default true;

    String why() default "because of some reasons";
}
