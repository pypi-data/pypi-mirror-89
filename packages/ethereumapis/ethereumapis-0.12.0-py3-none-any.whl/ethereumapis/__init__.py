
import sys
import ethereumapis
import ethereumapis._internal.github
import ethereumapis._internal.google.api

sys.modules["eth"] = ethereumapis
sys.modules["github"] = ethereumapis._internal.github
sys.modules["google.api"] = ethereumapis._internal.google.api

__all__ = ["v1", "v1alpha1"]
