data "aws_route53_zone" "madoc" {
  name         = "${var.madoc_domain}."
  private_zone = false
}

resource "aws_route53_record" "madoc" {
  zone_id = data.aws_route53_zone.madoc.zone_id
  name    = var.madoc_domain
  type    = "A"
  ttl     = "3600"
  records = [aws_eip.madoc.public_ip]
}