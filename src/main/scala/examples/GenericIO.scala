package examples

import cats.Monad
import cats.effect.std.Console
import cats.syntax.all._

object GenericIO {

  def example[F[_] : Monad : Console](str: String): F[String] = {
    val printer: F[Unit] = Console[F].println(str)
    (printer >> printer).as(str)
  }

}
