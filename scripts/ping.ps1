$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "..")

Push-Location $ProjectRoot
try {
    @'
from __future__ import annotations

import asyncio

from moodle_mcp.config.settings import settings
from moodle_mcp.moodle import APIFunction, get_moodle_api_data


async def main() -> None:
    settings.validate()
    data = await get_moodle_api_data(APIFunction.core_webservice_get_site_info)
    if not isinstance(data, dict):
        raise TypeError("Moodle returned an unexpected site-info response.")

    sitename = data.get("sitename", "Unknown Moodle site")
    userid = data.get("userid", "unknown user")
    release = data.get("release")
    version = data.get("version")

    print(f"Connected to {sitename} as Moodle user {userid}.")
    if release or version:
        print(f"Moodle release={release or 'unknown'} version={version or 'unknown'}")


asyncio.run(main())
'@ | uv run python -

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}
finally {
    Pop-Location
}
