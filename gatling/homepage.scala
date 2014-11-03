
import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class HomepageSimulation extends Simulation {

	val httpProtocol = http
		.baseURL("http://osmrtcheck.quiedeville.org")
		.inferHtmlResources()
		.acceptHeader("""text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8""")
		.acceptEncodingHeader("""gzip, deflate""")
		.acceptLanguageHeader("""fr-fr,en-us;q=0.7,en;q=0.3""")
		.userAgentHeader("""Mozilla/5.0 (X11; Linux i686 on x86_64; rv:10.0.7) Gecko/20100101 Firefox/10.0.7 Iceweasel/10.0.7""")

	val headers_2 = Map("""Accept""" -> """image/png,image/*;q=0.8,*/*;q=0.5""")

	val headers_6 = Map(
		"""Accept""" -> """application/json, text/javascript, */*; q=0.01""",
		"""X-Requested-With""" -> """XMLHttpRequest""")

    val uri5 = """http://osmrtcheck.quiedeville.org"""

	val scn = scenario("HomepageSimulation")
		.exec(http("request_0")
			.get("http://" + uri5 + """/"""))
		.pause(13)
		.exec(http("request_1")
			.get("""/""")
			.resources(http("request_2")
			.get(uri5 + """/favicon.ico""")
			.headers(headers_2)
			.check(status.is(404)),
            http("request_3")
			.get(uri5 + """/favicon.ico""")
			.check(status.is(404))))
		.pause(4)
		.exec(http("request_6")
			.get(uri5 + """/alert/zone/2/data.geojson""")
			.headers(headers_6))
		.pause(21)
		.exec(http("request_10")
			.get("""/alerts/"""))
		.pause(1)
		.exec(http("request_11")
			.get("""/rules/""")
			.resources(http("request_12")
			.get(uri5 + """/static/fonts/glyphicons-halflings-regular.woff""")))

	setUp(scn.inject(atOnceUsers(1))).protocols(httpProtocol)
}
