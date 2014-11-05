package frt.evt

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

object Events {

  val list = http("""/events/""").get("""/events/""")
             
}
