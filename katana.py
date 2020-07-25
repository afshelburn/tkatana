
import mido
import time
from time import sleep
import threading
import sys
from globals import *
import syslog

class Katana:

    def __init__( self, portname, channel, clear_input=False ):
        self.outport = mido.open_output( portname )
        self.inport = mido.open_input( portname )

        self.sysex = mido.Message('sysex')

        self.pc = mido.Message('program_change')
        self.pc.channel = channel

        self.cc = mido.Message('control_change')
        self.cc.channel = channel

        self.chunk_count = 0

        self.current_volume = 0

        self.busy = 1
        
        # Thread synchronization around incoming MIDI data. Used only
        # in the case where a single message is expected.  We need to use
        # a different approach for bulk sysex dumps where an arbitrary 
        # number of replies may be sent.
        self.receive_cond = threading.Condition()
        self.addr = []
        self.data = []

        if clear_input: 
            self._clear_input()

        # Since mido callbacks take only a single parameter, bind
        # the current object into a closure
        self.inport.callback = lambda msg: self._post( msg )

    # Drain incoming USB buffer by doing polled reads over
    # five seconds
    def _clear_input( self ):
        # Force off edit mode
        # self.send_sysex_data( EDIT_OFF )
        start = time.time()
        while True:
            msg = self.inport.poll()
            now = time.time()
            if now - start > 5:
                break

    # Called by rtmidi in a separate thread to absorb bulk response
    def _post( self, msg ):
        if msg.type != 'sysex':
            syslog.syslog( "Err: Saw msg type: " + msg.type )

        self.receive_cond.acquire()

        curr_addr = msg.data[7:11]
        self.addr.append( curr_addr )

        curr_data = msg.data[11:-1]
        self.data.append( curr_data )

        # Signal the consumer if we've reached the expected number of messages.
        self.chunk_count += 1
        if self.chunk_count == self.target_count:
            self.chunk_count = 0
            self.receive_cond.notify()

        self.receive_cond.release()

    # Concatenate caller's prefix and message, add checksum and send
    # as sysex message. Handles both store and query commands.
    def _send( self, prefix, msg ):
        # print( "DEBUG: msg = ", msg )
        # Calculate Roland cksum on msg only
        accum = 0
        for byte in msg:
            accum = (accum + byte) & 0x7f
            cksum = (0x80 - accum) & 0x7f

        data = []
        data.extend( prefix )
        data.extend( msg )
        data.append( cksum )
        #print(str(data))
        self.sysex.data = data
        self.outport.send( self.sysex )

    # Convenience method for store commands. Takes address and
    # optional data payload.
    def send_sysex_data( self, addr, data=None ):
        if data == None:
            msg = addr
        else:
            msg = list( addr )
            msg.extend( data )

        self._send( SEND_PREFIX, msg )

    # Encode scalar length into 4-byte sysex value
    @staticmethod
    def encode_scalar( len ):
        result = [0x00, 0x00, 0x00, 0x00]
        result[3] = len % 0x80
        result[2] = (len // 0x80) % 0x80
        result[1] = (len // 0x4000) % 0x80
        result[0] = (len // 0x200000) % 0x80
        return result

    def query_color_assignment(self):
        res = []
        res.append(self.query_sysex_byte(BOOST_ASSIGN_G))
        res.append(self.query_sysex_byte(BOOST_ASSIGN_R))
        res.append(self.query_sysex_byte(BOOST_ASSIGN_O))
        res.append(self.query_sysex_byte(MOD_ASSIGN_G))
        res.append(self.query_sysex_byte(MOD_ASSIGN_R))
        res.append(self.query_sysex_byte(MOD_ASSIGN_O))
        res.append(self.query_sysex_byte(FX_ASSIGN_G))
        res.append(self.query_sysex_byte(FX_ASSIGN_R))
        res.append(self.query_sysex_byte(FX_ASSIGN_O))
        res.append(self.query_sysex_byte(DELAY_ASSIGN_G))
        res.append(self.query_sysex_byte(DELAY_ASSIGN_R))
        res.append(self.query_sysex_byte(DELAY_ASSIGN_O))
        res.append(self.query_sysex_byte(REVERB_ASSIGN_G))
        res.append(self.query_sysex_byte(REVERB_ASSIGN_R))
        res.append(self.query_sysex_byte(REVERB_ASSIGN_O))
        return res

    def assign_boost(self, clr, c):
        addr = self.effective_addr(BOOST_ASSIGN_G, clr)
        self.send_sysex_data(addr, (c,))

    def assign_mod(self, clr, c):
        addr = self.effective_addr(MOD_ASSIGN_G, clr)
        self.send_sysex_data(addr, (c,))

    def assign_fx(self, clr, c):
        addr = self.effective_addr(FX_ASSIGN_G, clr)
        self.send_sysex_data(addr, (c,))

    def assign_delay(self, clr, c):
        addr = self.effective_addr(DELAY_ASSIGN_G, clr)
        self.send_sysex_data(addr, (c,))

    def assign_reverb(self, clr, c):
        addr = self.effective_addr(REVERB_ASSIGN_G, clr)
        self.send_sysex_data(addr, (c,))

    def boost_color(self, c):
        #d = (0x00,0x00,0x00,0x01)
        self.send_sysex_data(BOOST_COLOR,(c,))

    def mod_color(self, c):
        #d = (0x00,0x00,0x00,0x01)
        self.send_sysex_data(MOD_COLOR,(c,))

    def fx_color(self, c):
        #d = (0x00,0x00,0x00,0x01)
        self.send_sysex_data(FX_COLOR,(c,))

    def delay_color(self, c):
        #d = (0x00,0x00,0x00,0x01)
        self.send_sysex_data(DELAY_COLOR,(c,))

    def reverb_color(self, c):
        #d = (0x00,0x00,0x00,0x01)
        self.send_sysex_data(REVERB_COLOR,(c,))

    def query_boost_color(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(BOOST_COLOR)

    def query_mod_color(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(MOD_COLOR)

    def query_fx_color(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(FX_COLOR)

    def query_delay_color(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(DELAY_COLOR)

    def query_reverb_color(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(REVERB_COLOR)

    def query_reverb_level(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(REVERB_COLOR)

    def query_boost_level(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(BOOST_LEVEL)

    def query_mod_level(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(MOD_LEVEL)

    def query_fx_level(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(FX_LEVEL)

    def query_delay_level(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(DELAY_LEVEL)

    def query_reverb_level(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(REVERB_LEVEL)

    def query_boost_type(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(BOOST_TYPE)

    def query_mod_type(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(MOD_TYPE)

    def query_fx_type(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(FX_TYPE)

    def query_delay_type(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(DELAY_TYPE)

    def query_reverb_type(self):
        #d = (0x00,0x00,0x00,0x01)
        return self.query_sysex_byte(REVERB_TYPE)

    def select_channel(self, ch):
        self.send_pc(ch)

    def set_boost(self, amount):
        self.send_sysex_data(BOOST_LEVEL,(amount,))
        #self.send_cc(16, amount)

    def set_mod(self, amount):
        self.send_cc(17, amount)

    def set_fx(self, amount):
        self.send_cc(18, amount)

    def set_delay(self, amount):
        self.send_sysex_data(DELAY_LEVEL,(amount,))

    def set_reverb(self, amount):
        self.send_sysex_data(REVERB_LEVEL,(amount,))

    def set_boost_sw(self, sw):
        self.send_sysex_data(BOOST_SW, (sw,))

    def set_mod_sw(self, sw):
        self.send_sysex_data(MOD_SW, (sw,))

    def set_fx_sw(self, sw):
        self.send_sysex_data(FX_SW, (sw,))

    def set_delay_sw(self, sw):
        self.send_sysex_data(DELAY_SW, (sw,))

    def set_reverb_sw(self, sw):
        self.send_sysex_data(REVERB_SW, (sw,))

    def query_boost_sw(self):
        return self.query_sysex_byte(BOOST_SW)

    def query_mod_sw(self):
        return self.query_sysex_byte(MOD_SW)

    def query_fx_sw(self):
        return self.query_sysex_byte(FX_SW)

    def query_delay_sw(self):
        return self.query_sysex_byte(DELAY_SW)

    def query_reverb_sw(self):
        return self.query_sysex_byte(REVERB_SW)

    def set_amp(self, amp):
        return self.send_sysex_data(QUERY_AMP, (amp,))

    def query_amp(self):
        return self.query_sysex_byte(QUERY_AMP)

#    def query_boost(self):
        


    @staticmethod
    def decode_array( ary ):
        return (ary[0] * 0x200000) + (ary[1] * 0x4000) + (ary[2] * 0x80) + ary[3]
    
    # Next (3) query methods return a two-element tuple in the general form:
    # [addrA, addrB, .. ], [ [dataA, .. ], [dataB, .. ], .. ]

    # For situations where we do not know the number of replies to be
    # expected. It appears that 5 seconds is enough time for Katana to
    # send a complete MIDI sysex dump.  Warning: If more data arrives 
    # after the timeout it will cause big problems when we attempt to
    # snapshot a preset.
    def get_bulk_sysex_data( self, msg, timeout=5 ):
        self.data = []
        self.addr = []

        self.target_count = 99
        self._send( QUERY_PREFIX, msg )
        sleep( timeout )
        return self.addr, self.data

    # Request sysex data by passing start address and length. This
    # method is generally for smaller, single-chunk messages.
    def query_sysex_data( self, addr, len ):
        self.receive_cond.acquire()

        self.data = []
        self.addr = []
        msg = list( addr )
        msg.extend( Katana.encode_scalar(len) )

        self.target_count = (len // 241) + 1
        self._send( QUERY_PREFIX, msg )
        
        result = self.receive_cond.wait(5)
        if not result:
            print("timeout")
            print(str(msg))
            #print(str(self.data))
            syslog.syslog( "Error: Timeout on cond wait" )

        self.receive_cond.release()

        return self.addr, self.data

    # Request sysex data (possibly requiring multiple chunks) by
    # passing first and last address of desired range. It is the
    # caller's responsibility to ensure the total response does not
    # span address discontinuities.  If that occurs the chunk count is
    # likely to be over-estimated and the operation will timeout.
    def query_sysex_range( self, first_addr, last_addr ):
        self.receive_cond.acquire()

        span = Katana.decode_array(last_addr) - Katana.decode_array(first_addr)
        offset = Katana.encode_scalar( span + 1 )
        
        self.data = []
        self.addr = []

        msg = list( first_addr )
        msg.extend( offset )

        # Calculate expected number of chunks.  Maximum chunk is 255 bytes
        # with max payload of 241 data bytes/
        self.target_count = ((span + 1) // 241) + 1
        self._send( QUERY_PREFIX, msg )
        result = self.receive_cond.wait(5)
        if not result:
            syslog.syslog( "Error: Timeout on cond wait" )

        self.receive_cond.release()

        return self.addr, self.data

    # Bias 4-byte sysex array by scalar value
    @staticmethod
    def effective_addr( base, offset ):
        base_scalar = Katana.decode_array( base )
        return Katana.encode_scalar( base_scalar + offset )
        
    # Request a single byte
    def query_sysex_byte( self, addr, offset=None ):
        if offset == None:
            eff = addr
        else:
            eff = Katana.effective_addr( addr, offset )

        (dummy, data) = self.query_sysex_data( eff, 1 )
        return data[0][0]
        
    # Send program change
    def send_pc( self, program ):
        self.pc.program = program
        self.outport.send( self.pc )

    # Send control change
    def send_cc( self, control, value ):
        self.cc.control = control
        self.cc.value = value
        self.outport.send( self.cc )

    # Convenience method to set amplifier volume
    def volume( self, value ):
        self.send_sysex_data( VOLUME_PEDAL_ADDR, (value,) )

    def mute(self):
        self.current_volume = self.query_sysex_byte( VOLUME_PEDAL_ADDR )
        print("Muting, current volume: " + str(self.current_volume))
        self.volume(0)

    def unmute(self):
        print("Unmuting, current volume: " + str(self.current_volume))
        self.volume(self.current_volume)

    # Cycle volume pedal gain to provide audible signal
    def signal( self ):
        # Get current volume pedal position
        current_volume = self.query_sysex_byte( VOLUME_PEDAL_ADDR )

        # Mute volume briefly
        self.send_sysex_data( VOLUME_PEDAL_ADDR, (0,)  )
        sleep( 0.3 )
        
        # Then cycle to 50% in case volume pedal was off when
        # save initiated.
        self.send_sysex_data( VOLUME_PEDAL_ADDR, (50,) )
        sleep( 0.3 )

        # Finally, restore current pedal position
        self.send_sysex_data( VOLUME_PEDAL_ADDR, (current_volume,) )

    def get_patch_names(self):
        names = []
        for i in range(9):
            rq = PATCH_NAME_BASE.copy()
            rq[1] = rq[1] + i
            addr = (rq[0],rq[1],rq[2],rq[3])
            name = self.query_sysex_data(addr,0x10)[1][0]
            res = ''.join(map(chr, name)) 
            print(res)
            time.sleep(0.01)
            names.append(res)
        return names
	

if __name__ == '__main__':
    for test in (PANEL_STATE_ADDR, CURRENT_PRESET_ADDR):
        decode = Katana.decode_array( test )
        encode = Katana.encode_scalar( decode )
        test_list = list(test)
        if test_list != encode:
            print( "Failed:", test_list, "!=", encode )
