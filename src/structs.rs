#[allow(dead_code)]

#[derive(Debug)]
struct Person<'a> {
    name: &'a str,
    age: u8
}

// Структура с двумя полями
#[derive(Debug)]
struct Point {
    x: f64,
    y: f64,
}

// Структуры могут быть использованы как поля другой структуры
#[derive(Debug)]
struct Rectangle {
    p1: Point,
    p2: Point,
}

fn rect_area(figure: Rectangle) -> f64 {
    let Rectangle{
        p1: Point{
            x: x1,
            y: y1,
        },
        p2: Point{
            x: x2,
            y: y2,
        }
    } = figure;

    return ((x1-x2) * (y1-y2)).abs();
}

fn square(p1: Point, width: f64) -> Rectangle {
    let p2 = Point{x: p1.x+width, y: p1.y+width};

    return Rectangle {p1,p2}
}

fn main() {
    // Создаём структуру `Point`
    let point: Point = Point { x: 0.3, y: 0.4 };

    println!("Площадь штуки: {:?}", rect_area(square(point, 10f64)));
}