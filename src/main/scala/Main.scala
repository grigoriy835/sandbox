import cats.effect.{IO, IOApp}
import examples.{StupidFizzBuzz}
import scala.concurrent.duration._
import cats.Monad
import cats.effect.std.Console
import cats.syntax.all._

object Main extends IOApp.Simple {
  val run: IO[Unit] = IO.println("lol")

  def example[F[_] : Monad : Console](str: String): F[String] = {
    val printer: F[Unit] = Console[F].println(str)
    (printer >> printer).as(str)
  }

}

//object Hello2 extends App {
////  println("Hello, world")
//
//  def example[F[_] : Monad : Console](str: String): F[String] = {
//    val printer: F[Unit] = Console[F].println(str)
//    (printer >> printer).as(str)
//  }
//
//  val tt = example[IO]("avada kedavra")
//
//  tt.start
//}