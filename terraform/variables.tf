variable "db_username" {
    description = "Database administrator username"
    type = string
    default = "postgres"
}

variable "db_password" {
    description = "Database administrator password"
    type = string
    sensitive = true
}