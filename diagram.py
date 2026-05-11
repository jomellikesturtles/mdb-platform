

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.analytics import Spark
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.aggregator import Fluentd
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.network import Traefik
from diagrams.onprem.compute import Server
from diagrams.aws.compute import EC2
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.generic.blank import Blank
from diagrams.aws.engagement import SES
from diagrams.saas.chat import Slack
from diagrams.onprem.network import Internet


graph_attr = {
    # "concentrate": "true",
    "compound": "true",
    "splines": "spline",
    "fontsize": "20",
    "bgcolor": "white",
}

# Color Palette for Architecture Logic
SYNC_COLOR = "royalblue"     # Direct Request/Response (REST/gRPC)
ASYNC_COLOR = "darkgreen"    # Event Streams (Kafka)
AUTH_COLOR = "firebrick"     # Security/Auth flows
INFRA_COLOR = "gray30"       # Database/Storage

# run with python3 diagram.py or python diagram.py
with Diagram("Media Database", show=False, graph_attr=graph_attr):

#     # Connect nodes but point the arrow to the clusters
#     groupA[0] >> Edge(ltail="cluster_Source Cluster", lhead="cluster_Target Cluster") >> groupB[0]
    crawler_service = Server("crawler-service")
    notification_service = Server("notification-service")
    
    # Frontend
    with Cluster("Frontend Layer"):
        web_app = Server("web-app\n(users)")
        admin_web_app = Server("admin-web-app\n(admin)")
        
    # Ingress
    ingress = Traefik("Traefik\n(API Gateway / Reverse Proxy)")

    # BFF LAyer
    with Cluster("BFF Services"):
        mdb_bff_service = Server("mdb-bff-service")
        mdb_admin_bff_service = Server("mdb-admin-bff")
        bff_services_group = [mdb_bff_service, mdb_admin_bff_service]

    # metrics = Prometheus("metric")
    # metrics << Grafana("monitoring")

    with Cluster("Gateway Service Cluster"):
        user_data_gateway_service = Server("user-data-gateway-service")
        media_data_gateway_service = Server("media-data-gateway-service")
        gateway_services_group = [
            media_data_gateway_service,
            user_data_gateway_service]

    with Cluster("Cache HA"):
        primary = Redis("session")
        primary - Redis("replica")
    #     primary - Redis("replica") << metrics

    # with Cluster("Database HA"):
    #     primary = PostgreSQL("users")
    # #     primary - PostgreSQL("replica") << metrics
    #     gateway_services_group[0] >> primary

    # aggregator = Fluentd("logging")
    
    kafka = Kafka("Event Backbone\n(Apache Kafka)")
    # aggregator >> kafka >> Spark("analytics")
    

    
    # for node in bff_services_group:
    #     node >> gateway_services_group
    # >> gateway_services_group >> aggregator

    with Cluster("Storage"):
        user_db = PostgreSQL("Postgres\nUsers DB")
        media_db = PostgreSQL("Postgres\nMedia DB")
        object_storage = SimpleStorageServiceS3("MinIO\n(Object Storage)")
    
    with Cluster("Overview"):
        overview = Server("Overview\nPortfolio")
        storage = SimpleStorageServiceS3("S3")
    
    with Cluster("External Services"):
        slack = Slack("Slack Webhook")
        email = SES("Email Provider (SES)")

    # dashed, solid, dotted
    
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"

    [web_app, admin_web_app] >> Edge(color=SYNC_COLOR) >> ingress >> Edge(color=SYNC_COLOR) >> bff_services_group
    bff_services_group[1] >> Edge(color=SYNC_COLOR) >> primary
    # bff_services_group[0] >> primary
    bff_services_group >> Edge(color=SYNC_COLOR) >> kafka
    Internet("TMDB,Imdb") >> crawler_service >> media_data_gateway_service
    mdb_bff_service >> Edge(color=SYNC_COLOR, label="Direct Query (REST/gRPC)") >> [user_data_gateway_service, media_data_gateway_service]
    # mdb_admin_bff_service >> Edge(color=SYNC_COLOR, label="Direct Query (REST/gRPC)") >> [user_data_gateway_service, media_data_gateway_service]
    media_data_gateway_service >> Edge(color=SYNC_COLOR) >> media_db
    user_data_gateway_service >> Edge(color=SYNC_COLOR) >> user_db
    kafka >> Edge(color=INFRA_COLOR, style=DASHED) >> [mdb_admin_bff_service,notification_service]
    notification_service >> Edge(color=SYNC_COLOR) >> [email,slack]
    overview << Edge(color=SYNC_COLOR, label="app download, large files") << storage
    # mdb_bff_service >> Edge(color=SYNC_COLOR, label="REST") >> Server("Search Engine")