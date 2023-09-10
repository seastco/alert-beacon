# Earthquake Alert

Earthquake Alert is an SMS alert system for 6.1+ magnitude earthquakes on the United States west coast, primarily in anticipation of this century's _Big One_ events.

The hosted implementation is querying the United States Geological Survey (USGS) system every 3 minutes using AWS Lambda and EventBridge Scheduler. An earthquake takes 2-8 minutes to be processed and posted to the USGS system, so to account for this the script has a lookback period of 10 minutes. Given that the query happens every 3 minutes, this may result in a duplicate alert or two.

To subscribe, email me your phone number at seastco@proton.me. If you'd like to host this yourself, the lambda package is available under lambda_package.zip.

### [Magnitude scale](https://en.wikipedia.org/wiki/Moment_magnitude_scale)
- 2.5 or less - Usually not felt, but can be recorded by seismograph.
- 2.5 to 5.4 - Often felt, but only causes minor damage.
- 5.5 to 6.0 - Slight damage to buildings and other structures.
- 6.1 to 6.9 - May cause a lot of damage in very populated areas.
- 7.0 to 7.9 - Major earthquake. Serious damage.
- 8.0 or greater - Great earthquake. Can totally destroy communities near the epicenter.

California has experienced six 6.1+ magnitude earthquakes since 2000. Oregon and Washington have each experienced one.

### [The Big One](https://laist.com/news/climate-environment/the-big-one-is-coming-to-southern-california-this-is-your-survival-guide)

The Ridgecrest earthquakes that hit on July 4th and 5th, 2019 with a magnitude 6.4 and 7.1, respectively, were the most recent major earthquakes in Southern California. The 7.1 lasted 12 seconds and was felt by about 30 million people. More than 6,000 lost power. These earthquakes followed a 25 year "quiet period" after Northridge, which was a 6.7 magnitude earthquake that killed 58, injured more than 9,000 and caused more than $49 billion in economic loss. That quake lasted less than 20 seconds.

_The Big One_ will be at least 11 times stronger than the Ridgecrest earthquake and 44 times stronger than Northridge.

According to [The ShakeOut Scenario](https://pubs.usgs.gov/of/2008/1150/), a 7.8 earthquake hitting along the southern San Andreas fault on a non-windy day at about 9 a.m. will unfold, approximately, like this:
- 1,800 people will die.
- 1,600 fires will ignite and most of those will be large fires.
- 750 people will be trapped inside buildings with complete collapse.
- 270,000 people will be immediately displaced from their homes.
- 50,000 people will need ER care.
- 11 days out, people will start to drink more.
- Search and rescue efforts will last for 19 days.

### [The Really Big One](https://www.newyorker.com/magazine/2015/07/20/the-really-big-one)

Under pressure from oceanic plate Juan de Fuca, the stuck edge of North America is bulging upward and compressing eastward at the rate of millimetres a year. But it cannot do so indefinitely. There is a backstop—the craton, that ancient unbudgeable mass at the center of the continent—and, sooner or later, North America will rebound like a spring. If only the southern part of the Cascadia subduction zone gives way, the magnitude of the resulting quake will be somewhere between 8.0 and 8.6. If the entire zone gives way at once, an event that seismologists call a full-margin rupture, the magnitude will be somewhere between 8.7 and 9.2. That’s the _Really Big One._

By the time the shaking has ceased and the tsunami has receded, the Northwest coast of the United States will be unrecognizable. The area of impact will cover some 140,000 square miles, including Seattle, Tacoma, Portland, Eugene, Salem (the capital city of Oregon), Olympia (the capital of Washington), and some 7 million people.

Kenneth Murphy, who directs fema’s Region X, the division responsible for Oregon, Washington, Idaho, and Alaska, says, "Our operating assumption is that everything west of Interstate 5 will be toast."
