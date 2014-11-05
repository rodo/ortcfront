
import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

import frt.hmp._
import frt.al._


class HomepageSimulation extends Simulation {

	val httpProtocol = http
		.baseURL("http://osmrtcheck.quiedeville.org")
		.inferHtmlResources()
		.acceptHeader("""text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8""")
		.acceptEncodingHeader("""gzip, deflate""")
		.acceptLanguageHeader("""fr-fr,en-us;q=0.7,en;q=0.3""")
		.userAgentHeader("""Mozilla/5.0 (X11; Linux i686 on x86_64; rv:10.0.7) Gecko/20100101 Firefox/10.0.7 Iceweasel/10.0.7""")

	val headers_6 = Map(
		"""Accept""" -> """application/json, text/javascript, */*; q=0.01""",
		"""X-Requested-With""" -> """XMLHttpRequest""")

    val headers_2 = Map("""Accept""" -> """image/png,image/*;q=0.8,*/*;q=0.5""")

    val uri5 = """http://osmrtcheck.quiedeville.org"""

    val homepage = frt.hmp.Homepage.home
    val alerts_list = frt.al.Alerts.list

    val scn = scenario("HomepageSimulation")
                    .exec(homepage)
                    .exec(alerts_list)

	setUp(scn.inject(atOnceUsers(1))).protocols(httpProtocol)
}
