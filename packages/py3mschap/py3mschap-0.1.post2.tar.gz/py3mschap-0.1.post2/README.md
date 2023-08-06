# py3mschap

First of all I hereby acknowledge this is not my original work. This repo 
is based on work of `jamiesun.net@gmail.com`, original repo is
 
[https://github.com/talkincode/pymschap](https://github.com/talkincode/pymschap). 
 
### Why I decided to fork it and rename it

 * I needed python3 pip package
 * repo is left with much of care, where I need my own code base with possibility to extend it
 * I have quite bad experience with pr->fix->pip cycle flow

### What you can expect here  
If everything is running ok, probably some more from radius related mechanisms implemented 
in my simple radius **testing mini-server** [raok](https://github.com/astibal/raok).
This module will be used there and via pip3 maintained for further improvements.


 ##### Original example provided by Jamie


    def verify_radius_request(ms_chap_response,authenticator_challenge,username,userpwd,secret,authenticator):
        import six
        from pymschap import mschap, mppe
        result = {}
        if len(ms_chap_response)!=50:
            raise Exception("Invalid MSCHAPV2-Response attribute length")
        # if isinstance(userpwd, six.text_type):
        #     userpwd = userpwd.strip().encode('utf-8')
        
        nt_response = ms_chap_response[26:50]
        peer_challenge = ms_chap_response[2:18]
        nt_resp = mschap.generate_nt_response_mschap2(
            authenticator_challenge,
            peer_challenge,
            username,
            userpwd,
        )
        if nt_resp == nt_response:
            auth_resp = mschap.generate_authenticator_response(
                userpwd,
                nt_response,
                peer_challenge,
                authenticator_challenge,
                username
            )
            result['MS-CHAP2-Success'] = auth_resp
            result['MS-MPPE-Encryption-Policy'] = '\x00\x00\x00\x01'
            result['MS-MPPE-Encryption-Type'] = '\x00\x00\x00\x06'
            mppeSendKey, mppeRecvKey = mppe.mppe_chap2_gen_keys(userpwd, nt_response)
            send_key, recv_key = mppe.gen_radius_encrypt_keys(
                mppeSendKey,
                mppeRecvKey,
                secret,
                authenticator)
            result['MS-MPPE-Send-Key'] = send_key
            result['MS-MPPE-Recv-Key'] = recv_key
        else:
            result['Reply-Message'] = "E=691 R=1 C=%s V=3 M=<password error>" % ('\0' * 32)
            
        return result
        