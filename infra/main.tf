terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "app" {
  name         = var.image_name
  keep_locally = true
}

resource "docker_container" "staging" {
  name  = var.container_name
  image = docker_image.app.image_id

  restart = "unless-stopped"

  ports {
    internal = var.container_port
    external = var.host_port
  }

  networks_advanced {
    name = var.network_name
  }

  healthcheck {
    test         = ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
    interval     = "10s"
    timeout      = "5s"
    retries      = 5
    start_period = "10s"
  }
}