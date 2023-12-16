import re

def is_valid_ip_address(ip_address):
  """
  Überprüft, ob `ip_address` eine gültige IP-Adresse ist.

  Args:
    ip_address: Die IP-Adresse, die überprüft werden soll.

  Returns:
    True, wenn `ip_address` eine gültige IP-Adresse ist, False sonst.
  """

  parts = ip_address.split(".")
  if len(parts) != 4:
    return False

  for part in parts:
    if not re.match(r"^[0-9]{1,3}$", part):
      return False

  return True

def jsonify(programs):
  """
  Erstellt ein JSON-Objekt aus `programs`.

  Args:
    programs: Eine Liste von ProgramConfig-Objekten.

  Returns:
    Ein JSON-Objekt, das die Daten aus `programs` enthält.
  """

  return {
    "programs": [
      {
        "name": program,
      }
      for program in programs
    ]
  }
