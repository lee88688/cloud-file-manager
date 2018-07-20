<template>
    <transition enter-active-class="animated bounceInDown" leave-active-class="animated bounceOutUp">
        <div class="d-flex justify-content-center fixed-top mt-1" v-if="hasMessage" style="z-index: 1070;">
            <div style="min-width:50%;" class="alert text-center" v-bind:class="[ messageStyle ]">
                {{ messageContent }}
            </div>
        </div>
    </transition>
</template>

<script>
import { mapGetters } from 'vuex'
import { Messager } from '../lib/notification'

export default {
    computed: {
        ...mapGetters([
            'hasMessage',
            'firstMessage'
        ]),
        messageStyle() {
            let message = this.firstMessage
            if (!message) {
                return ''
            }
            switch (message.level) {
                case Messager.LEVEL.INFO: {
                    return 'alert-dark'
                }
                case Messager.LEVEL.WARNING: {
                    return 'alert-warning'
                }
                case Messager.LEVEL.ERROR: {
                    return 'alert-danger'
                }
                default: {
                    return 'alert-dark'
                }
            }
        },
        messageContent() {
            if (this.firstMessage) {
                return this.firstMessage.content
            }
            else {
                return ''
            }
        }
    }
}
</script>
