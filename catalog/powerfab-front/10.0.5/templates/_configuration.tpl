{{- define "redis.configuration" -}}
configmap:
  config:
    enabled: true
    data:
      POWERAPS_REST_ENDPOINT: {{ .Values.poweraps.env.powerApsBackend | quote }}
{{- end -}}