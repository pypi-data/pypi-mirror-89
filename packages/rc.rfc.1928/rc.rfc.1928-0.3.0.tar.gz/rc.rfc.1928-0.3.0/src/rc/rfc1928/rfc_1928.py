
__author__    = 'Andre Merzky <andre@merzky.net>'
__license__   = 'GNU AGPL.v3 *or* Commercial License'
__copyright__ = 'Copyright (C) 2019, RADICAL-Consulting UG'


import socket
import struct


# =-----------------------------------------------------------------------------
#
class RFC_1928(object):
    '''
    Simple and limited implementation of SOCKS5 as specified in RFC.1928
    (https://www.ietf.org/rfc/rfc1928.txt)

    This implementation only supports unauthenticated SOCKS5 servers, and can
    only handle IPv4 addresses.
    '''

    # --------------------------------------------------------------------------
    #
    Version   = b'\x05'
    Null      = b'\x00'
    NoSuccess = b'\xff'


    # --------------------------------------------------------------------------
    #
    AuthNone     = b'\x00'
    AuthGSSAPI   = b'\x01'
    AuthUserPass = b'\x02'
    AuthError    = b'\xFF'

    # b'\x03' to b'7f': IANA ASSIGNED                  # unsupported
    # b'\x80' to b'fe': RESERVED FOR PRIVATE METHODS   # unsupported

    AuthMethods = {
            AuthNone     : 'NO AUTHENTICATION REQUIRED',
            AuthGSSAPI   : 'GSSAPI',
            AuthUserPass : 'USERNAME/PASSWORD',
            AuthError    : 'NO ACCEPTABLE METHODS',
    }


    # --------------------------------------------------------------------------
    #
    CmdConnect       = b'\x01'
    CmdBind          = b'\x02'
    CmdUDPAassociate = b'\x03'

    Commands = {
            CmdConnect       : 'CONNECT',
            CmdBind          : 'BIND',           # unsupported
            CmdUDPAassociate : 'UDP ASSOCIATE',  # unsupported
    }


    # --------------------------------------------------------------------------
    #
    RepSuccess     =  b'\x00'
    RepServError   =  b'\x01'
    RepDenied      =  b'\x02'
    RepNoNetwork   =  b'\x03'
    RepUnreachable =  b'\x04'
    RepRefused     =  b'\x05'
    RepTTL         =  b'\x06'
    RepUnsupported =  b'\x07'
    RepAddrError   =  b'\x08'

    # b'\x09 to b\xff' : unassigned

    Replies = {
            RepSuccess     :'succeeded',
            RepServError   :'general SOCKS server failure',
            RepDenied      :'connection not allowed by ruleset',
            RepNoNetwork   :'Network unreachable',
            RepUnreachable :'Host unreachable',
            RepRefused     :'Connection refused',
            RepTTL         :'TTL expired',
            RepUnsupported :'Command not supported',
            RepAddrError   :'Address type not supported',
    }


    # --------------------------------------------------------------------------
    #
    AddrIPv4   = b'\x01'
    AddrDomain = b'\x03'
    AddrIPv6   = b'\x04'

    AddressType = {
            AddrIPv4   : 'IP V4 address',
            AddrDomain : 'DOMAINNAME',     # unsupported
            AddrIPv6   : 'IP V6 address',  # unsupported
    }


    # --------------------------------------------------------------------------
    #
    @staticmethod
    def byteify(data):

        if isinstance(data, int):
            return struct.pack('B', data)

        if isinstance(data, str):
            ret = b''
            for c in data:
                ret += struct.pack('B', c)
            return ret

        raise TypeError('not an int or string type (%s)' % type(data))


    # --------------------------------------------------------------------------
    #
    def send_auth(self, channel, methods, *args):

        # get byte representation for request elements
        version   = self.Version
        n_methods = self.byteify(len(methods))
        b_methods = ''

        for method in methods:
            assert(method != self.AuthError)
            b_methods += method

        channel.write(version + n_methods + b_methods)
        resp = channel.read(2)

        # ensure valid reply and authentication
        assert(resp[0:1] == version)

        auth = resp[1:2]
        if auth == self.NoSuccess:
            raise RuntimeError('no valid auth method available')

        assert(auth in methods)

        return auth


    # --------------------------------------------------------------------------
    #
    def connect(self, channel, family, tgt_ip, tgt_port):

        # request connection to target address
        cmd  = self.CmdConnect
        rsv  = self.Null       # reserved
        atyp = self.AddrIPv4   # only support IPv4
        addr = socket.inet_pton(family, tgt_ip)

        channel.write(self.Version + cmd + rsv + atyp + addr)
        channel.write(struct.pack('>H', tgt_port))
        resp = channel.read(3)

        # ensure valid data and success
        assert(resp[0:1] == self.Version)
        assert(resp[1:2] == self.RepSuccess)
        assert(resp[2:3] == self.Null)   # reserved

        # get the bound address/port - we handle IPv4 addresses only
        p_atyp = channel.read(1)
        assert(self.AddrIPv4 == p_atyp)

        p_host = socket.inet_ntoa(channel.read(4))
        p_port = struct.unpack('>H', channel.read(2))[0]

        # do we also need to return p_atype?
        return p_host, p_port


    # --------------------------------------------------------------------------
    #
    def negotiate(self, channel, addr_type, tgt_host, tgt_port,
                  auth_method=None):

        if not auth_method:
            auth_method = self.AuthNone

        # only support connections with no authentication.
        self.send_auth(channel, methods=[auth_method])

        # resolve address (even if it is an IP  nunmber already)
        addrs = socket.getaddrinfo(tgt_host, tgt_port, socket.AF_UNSPEC,
                                   socket.SOCK_STREAM,
                                   socket.IPPROTO_TCP,
                                   socket.AI_ADDRCONFIG)

        # pick first valid address
        tgt_addr = addrs[0]
        family   = tgt_addr[0]
        tgt_ip   = tgt_addr[4][0]

        p_host, p_port = self.connect(channel, family, tgt_ip, tgt_port)

        # do we also need to return p_atype?
        return p_host, p_port


# ------------------------------------------------------------------------------
#
def socksify(channel, tgt_host, tgt_port):

    rfc = RFC_1928()
    return rfc.negotiate(channel, rfc.AddrIPv4, tgt_host, tgt_port, rfc.AuthNone)


# ------------------------------------------------------------------------------

