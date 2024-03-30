import toast, { type Renderable } from 'svelte-french-toast';
import InfoIcon from './components/InfoIcon.svelte';

const duration = 5000;
const position = "bottom-right";

export function successToast(message: Renderable){
    toast.success(message, {
        duration: duration,
        position: position,
    })
}

export function errorToast(message: Renderable){
    toast.error(message, {
        duration: duration,
        position: position,
    })
}

export function infoToast(message: Renderable){
    toast(message, {
        icon: InfoIcon,
        duration: duration,
        position: position,
    })
}
