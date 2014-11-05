package frt.hmp

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

object Homepage {

  val uri5 = """http://osmrtcheck.quiedeville.org"""

  val headers_2 = Map("""Accept""" -> """image/png,image/*;q=0.8,*/*;q=0.5""")

  val home = http("""homepage""").get(uri5 + """/""")
             
}
