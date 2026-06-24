variable "image_name" {
  description = "Nom complet de l'image Docker à déployer"
  type        = string
}

variable "container_name" {
  description = "Nom du conteneur staging"
  type        = string
  default     = "devops-group-api-staging"
}

variable "host_port" {
  description = "Port exposé sur la machine hôte"
  type        = number
  default     = 8002
}

variable "container_port" {
  description = "Port interne du conteneur"
  type        = number
  default     = 8000
}

variable "network_name" {
  description = "Nom du réseau Docker CI/CD"
  type        = string
  default     = "cicd-network"
}