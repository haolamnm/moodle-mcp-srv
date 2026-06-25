"""Diagnostic and availability response models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from moodle_mcp.models.courses import SiteInfo  # noqa: TC001

FeatureStatus = Literal["available", "missing_function", "unknown"]
DoctorStatus = Literal["ok", "warning", "error"]


class FeatureAvailability(BaseModel):
    feature: str
    status: FeatureStatus
    required_functions: list[str]
    missing_functions: list[str] = Field(default_factory=list)
    note: str | None = None


class ServerCapabilityReport(BaseModel):
    available_functions_known: bool
    expected_functions: list[str]
    available_functions: list[str]
    features: list[FeatureAvailability]


class DoctorCheck(BaseModel):
    name: str
    status: DoctorStatus
    message: str
    action: str | None = None


class DoctorReport(BaseModel):
    ok: bool
    site_info: SiteInfo | None
    checks: list[DoctorCheck]
    features: ServerCapabilityReport | None
    check_writes: bool = False


class WriteReceipt(BaseModel):
    dry_run: bool
    action: str
    target_type: str
    target_id: int | str
    reason: str | None = None
    would_change: list[str] = Field(default_factory=list)
    changed: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    moodle_function: str
