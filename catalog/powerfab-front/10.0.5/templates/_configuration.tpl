{{- define "redis.configuration" -}}
configmap:
  config:
    enabled: true
    data:
      POWERAPS_REST_ENDPOINT: {{ .Values.workload.main.podSpec.containers.main.env.POWERAPS_REST_ENDPOINT | quote }}
{{- end -}}
