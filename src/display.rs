use std::f32::consts::PI;
use std::fmt; // Импортируем `fmt`


fn formatters() {
    // Можно выравнивать текст, сдвигая его на указанную ширину.
    // Данный макрос отобразит в консоли
    // "     1". 5 пробелов и "1".
    let pi = PI;
    println!("{:.*}", 5, pi);

    // Можно добавить к цифрам пару нулей. Данный макрос выведет "000001".
    println!("{0:X>01$}", 1, 2);
}

#[derive(Debug)]
struct Color {
    red: u8,
    green: u8,
    blue: u8,
}

impl fmt::Display for Color {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "RGB ({0}, {1}, {2}) 0x{0:X>0width$}{1:X>0width$}{2:X>0width$}", self.red, self.green, self.blue, width=2)
    }
}

fn main() {
    for color in [
        Color { red: 128, green: 255, blue: 90 },
        Color { red: 0, green: 3, blue: 254 },
        Color { red: 0, green: 0, blue: 0 },
    ].iter() {
        // Поменяйте {:?} на {}, когда добавите реализацию
        // типажа fmt::Display
        println!("{}", *color)
    }
    formatters()
}
