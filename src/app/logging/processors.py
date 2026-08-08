import socket


def build_service_context_processor(service: str, env: str, version: str):
  static_context = {
    "service": service,
    "env": env,
    "version": version,
    "hostname": socket.gethostname(),
  }

  def add_service_context(logger, method_name, event_dict):
    for key, value in static_context.items():
      event_dict.setdefault(key, value)
    return event_dict

  return add_service_context
