from app import mongo
from app.models import route as route_model, routepoints as route_point_model
# get routepoints from RoutePoints collection

route_point_collection = mongo.db.RoutePoints
route_points = route_point_collection.find()
route_geometry = 'ek`GiljyRqAJ_BLk@DG_@AKk@Hq@HqDd@m@J{Dd@{C\\WDA?}@JG@}@HqCVQA??KADj@Df@BTrBdX@BB\\@L@HWBM@i@DM@q@D_ObAC\\?H?TAX?PEXEZK^M\\GNKNS\\SVSPEDAJOJMAcA^IBQJONAN?D@BBBLDfBTLB?JCRQAo@Kc@Ai@GI@MBI`@If@Il@@DOjBGn@@F?REBE^A^?`@?N@\\?L?B@V@T?F@f@@PBh@@PPbB@DJ^Pb@JNDPD`@FT|@zBr@|@h@n@ZTF?D?|@iAl@m@VQBEJGJG@?RK@AHGdAg@PId@Mh@If@@R@fATp@Lp@FRB^@v@?R?l@E^EB?RAR?xAKbAKXMFD@BDLDF?L@JRLHVT~@PzA@p@EfB?BGDGp@?V?LBh@Cj@A@?P?N?f@?`@FlBLdB@H?F@DDn@@PB\\BPRAVvCF\\I@OIi@Db@tCMDM@e@F]BC@SBS@I@WDM@M@M@E@M@I@E@M@G@G?K@E@A?C@C?C?BD@F@D?D@BMFGCG@E@C?C?I@E?C?E@C?C?C@C?A?E@G@A?m@Fq@HEFCFCFEFABCBCDEFADABKNILABEHA@ABWb@ABABCBCDADABEDCFA@ABA@ABGJCDCBCBCDA@C@ILEDK?EI}@@qCDU@C?A?G?K?g@@G@C?C?C?K?QAE?I@G?C?K?k@@W@W?a@@K?C?K?C@E?I?e@@W@O?C?K@I?JV`@lAA@s@cBsAl@n@~AC?o@}AMa@YFAh@?DADADC@G@E?KGMGIEEGMQCGAO?M@UBS@QBKDIDKAECOEQGSQa@EECCCEESAMEKGIWWEICIEUCGIKKIMIMMCGAK?WAIEU?U?KACIMOSMSKYCECEK[EIEEYOKGAE?E@Q?SAMCEY[CGAGAM?UAGGMEQIOEIAME]KMGOIMQUGQMUKOEKAIISIWCOAE@E@K@GAEMWAGCMCGECGCGACCCGGKGICK?I@KAMIQIMEMIQGGGC[MSICE?G@[CSCGGG]SWK[KSIOGGEKGK?IBM@E?KAW?Y@YDi@JUDIBWJIDIFE@E@KSIc@i@RaBb@wARM@}CJE?eBD]@gCT_ADU@G[EOGs@AMFw@Ts@PYrAcBb@q@l@qA\\_ANc@Jk@@Q@YGs@'
nearest_points = route_point_model.RoutePoint.filter_route_points(route_points, route_geometry)
# print(nearest_points)
for i,point in enumerate(nearest_points):
    print(i,point)
    print()