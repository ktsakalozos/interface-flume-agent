# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class FlumeRequires(RelationBase):
    scope = scopes.UNIT

    @hook('{requires:flume-agent}-relation-joined')
    def joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.connected')

    @hook('{requires:flume-agent}-relation-changed')
    def changed(self):
        conv = self.conversation()
        if self.get_flume_ip() and self.get_flume_port() \
           and self.get_flume_protocol():
            conv.set_state('{relation_name}.available')

    @hook('{requires:flume-agent}-relation-departed')
    def departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.connected')
        conv.remove_state('{relation_name}.available')

    def get_flume_ip(self):
        return self.conversations()[0].get_remote('private-address')

    def get_flume_port(self):
        return self.conversations()[0].get_remote('port')

    def get_flume_protocol(self):
        return self.conversations()[0].get_remote('protocol')
