output "app_url" {
  description = "URL de l'application staging"
  value       = "http://localhost:${var.host_port}"
}

output "health_url" {
  description = "URL du healthcheck staging"
  value       = "http://localhost:${var.host_port}/health"
}

output "container_name" {
  description = "Nom du conteneur staging"
  value       = docker_container.staging.name
}

output "network_name" {
  description = "Nom du réseau Docker utilisé"
  value       = var.network_name
}