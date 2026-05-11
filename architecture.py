from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.network import Traefik
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import PostgreSQL
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.onprem.compute import Server
# from diagrams.onprem.security import Keycloak
# from diagrams.onprem.search import Search
from diagrams.aws.compute import EC2
from diagrams.aws.engagement import SES
from diagrams.saas.chat import Slack

graph_attr = {
    "compound": "true",
    "splines": "spline",
    "fontsize": "20",
    "bgcolor": "white"
}

with Diagram("MDB Platform Architecture", show=False, filename="architecture", graph_attr=graph_attr, direction="TB"):
    
    # External Notifications (Out of VPC)
    with Cluster("External Services"):
        slack = Slack("Slack Webhook")
        email = SES("Email Provider (SES)")

    with Cluster("AWS Cloud / VPC"):
        
        # Frontend Layer
        with Cluster("Frontend Layer"):
            web_app = EC2("mdb-web-app\n(Users)")
            admin_app = EC2("mdb-admin-web-app\n(Internal)")

        # Ingress
        ingress = Traefik("Traefik\n(API Gateway / Reverse Proxy)")

        # API & BFF Layer
        with Cluster("API Layer & BFFs"):
            bff_user = Server("mdb-bff-service")
            bff_admin = Server("mdb-admin-bff-service")
            bff_group = [bff_user, bff_admin]

        # Event Backbone
        kafka = Kafka("Event Backbone\n(Apache Kafka)")

        # Crawler
        crawler = Server("mdb-crawler-service")

        # Domain Services Layer
        with Cluster("Domain Services Layer"):
            user_gw = Server("user-data-gateway-service")
            media_gw = Server("media-data-gateway-service")
            domain_group = [user_gw, media_gw]

        # Notification Service
        notifier = Server("notification-service")

        # Infrastructure / Persistence
        with Cluster("Infrastructure & Storage"):
            # auth = Keycloak("Keycloak\n(Auth/IAM)")
            user_db = PostgreSQL("Postgres\n(Users DB)")
            media_db = PostgreSQL("Postgres\n(Media DB)")
            object_store = SimpleStorageServiceS3("MinIO\n(Object Storage)")
            # search_engine = Search("Meilisearch\n(Search Engine)")

        # --- Connections ---

        # Frontend to Ingress
        [web_app, admin_app] >> ingress
        
        # Ingress to BFFs
        ingress >> bff_group

        # BFFs to Kafka (Produce)
        bff_user >> Edge(label="Produce") >> kafka
        
        # Crawler to Kafka (Produce)
        crawler >> Edge(label="Produce") >> kafka

        # Domain Services to Kafka (Consume/Produce)
        kafka >> Edge(label="Consume") >> media_gw
        user_gw >> Edge(label="Produce") >> kafka

        # Kafka to Notification Service
        kafka >> Edge(label="Consume") >> notifier

        # BFF to Search Engine
        # bff_admin >> Edge(label="REST/gRPC") >> search_engine

        # Notification to Domain Services
        notifier >> Edge(label="REST/gRPC") >> domain_group

        # Domain Services to Infrastructure
        # user_gw >> auth
        user_gw >> user_db
        media_gw >> media_db
        media_gw >> object_store

        # Notification to External
        notifier >> [slack, email]
