// This file provides type definitions for UI components

declare module '@/components/ui/button' {
  import { Component } from 'vue'
  const Button: Component
  export { Button }
}

declare module '@/components/ui/textarea' {
  import { Component } from 'vue'
  const Textarea: Component
  export { Textarea }
}

declare module '@/components/ui/avatar' {
  import { Component } from 'vue'
  const Avatar: Component
  const AvatarFallback: Component
  const AvatarImage: Component
  export { Avatar, AvatarFallback, AvatarImage }
}

declare module '@/components/ui/toast/use-toast' {
  interface ToastOptions {
    title?: string
    description?: string
    variant?: 'default' | 'destructive'
  }

  interface ToastReturn {
    toast: (options: ToastOptions) => void
  }

  export function useToast(): ToastReturn
}
