$ErrorActionPreference = 'Stop'

# Generate a Python-Flask skeleton from OpenAPI using Swagger Codegen v3.
$JAR = Join-Path $PSScriptRoot 'swagger-codegen-cli.jar'
$OUTPUT = Join-Path $PSScriptRoot 'generated-flask-server'
$SPEC = Join-Path $PSScriptRoot 'openapi.yaml'

if (-not (Test-Path $JAR)) {
  Invoke-WebRequest `
    -Uri 'https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/3.0.52/swagger-codegen-cli-3.0.52.jar' `
    -OutFile $JAR
}

java -jar $JAR generate `
  -i $SPEC `
  -l python-flask `
  -o $OUTPUT

Write-Host "Generated server in: $OUTPUT"
