from __future__ import absolute_import, division, print_function

from telnyx.api_resources.abstract import ListableAPIResource


class RegulatoryRequirement(ListableAPIResource):
    OBJECT_NAME = "regulatory_requirement"
