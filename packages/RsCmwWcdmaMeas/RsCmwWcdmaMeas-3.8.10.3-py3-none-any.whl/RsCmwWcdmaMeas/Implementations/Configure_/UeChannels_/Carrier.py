from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal.RepeatedCapability import RepeatedCapability
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Carrier:
	"""Carrier commands group definition. 6 total commands, 5 Sub-groups, 0 group commands
	Repeated Capability: Carrier, default value after init: Carrier.Nr1"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("carrier", core, parent)
		self._base.rep_cap = RepeatedCapability(self._base.group_name, 'repcap_carrier_get', 'repcap_carrier_set', repcap.Carrier.Nr1)

	def repcap_carrier_set(self, enum_value: repcap.Carrier) -> None:
		"""Repeated Capability default value numeric suffix.
		This value is used, if you do not explicitely set it in the child set/get methods, or if you leave it to Carrier.Default
		Default value after init: Carrier.Nr1"""
		self._base.set_repcap_enum_value(enum_value)

	def repcap_carrier_get(self) -> repcap.Carrier:
		"""Returns the current default repeated capability for the child set/get methods"""
		# noinspection PyTypeChecker
		return self._base.get_repcap_enum_value()

	@property
	def edpdch(self):
		"""edpdch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_edpdch'):
			from .Carrier_.Edpdch import Edpdch
			self._edpdch = Edpdch(self._core, self._base)
		return self._edpdch

	@property
	def edpcch(self):
		"""edpcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_edpcch'):
			from .Carrier_.Edpcch import Edpcch
			self._edpcch = Edpcch(self._core, self._base)
		return self._edpcch

	@property
	def hsDpcch(self):
		"""hsDpcch commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_hsDpcch'):
			from .Carrier_.HsDpcch import HsDpcch
			self._hsDpcch = HsDpcch(self._core, self._base)
		return self._hsDpcch

	@property
	def dpdch(self):
		"""dpdch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpdch'):
			from .Carrier_.Dpdch import Dpdch
			self._dpdch = Dpdch(self._core, self._base)
		return self._dpdch

	@property
	def dpcch(self):
		"""dpcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_dpcch'):
			from .Carrier_.Dpcch import Dpcch
			self._dpcch = Dpcch(self._core, self._base)
		return self._dpcch

	def clone(self) -> 'Carrier':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Carrier(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
