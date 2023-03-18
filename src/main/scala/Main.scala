import cats.effect.{IO, IOApp}
import examples.{StupidFizzBuzz}

object Main extends IOApp.Simple {
  val run: IO[Unit] = IO.println("lol")
}

//object Hello2 extends App {
//  println("Hello, world")
//}