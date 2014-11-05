package frt.rul

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

object Rules {

  val list = http("""/rules/""").get("""/rules/""")
             
}
