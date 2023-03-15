import cats.effect.{IO, IOApp}
import examples.StupidFizzBuzz

object Main extends IOApp.Simple {
  val run: IO[Unit] = StupidFizzBuzz.run
}