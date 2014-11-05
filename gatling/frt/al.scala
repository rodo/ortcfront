package frt.al

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

object Alerts {

  val list = http("""homepage""").get("""/alerts/""")
             
}
