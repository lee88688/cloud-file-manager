<template>
    <transition enter-active-class="animated bounceInDown" leave-active-class="animated bounceOutUp">
        <div class="d-flex justify-content-center fixed-top mt-1" v-if="hasMessage">
            <div style="min-width:50%;" class="alert text-center" v-bind:class="[ messageStyle ]">
                {{ messageContent }}
                <button type="button" class="close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        </div>
    </transition>
</template>

<script>
import { mapGetters } from 'vuex'
import { INFO, WARNING, ERROR } from '../lib/notification'

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
                case INFO: {
                    return 'alert-dark'
                }
                case WARNING: {
                    return 'alert-warning'
                }
                case ERROR: {
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
