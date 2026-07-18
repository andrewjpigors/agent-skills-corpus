---
name: react-patterns
description: >
  Build React frontends with Inertia.js, TypeScript, and modern component patterns.
  Use when creating React components, Inertia pages, layouts, hooks, context providers,
  or integrating with a Laravel backend. Covers Inertia.js page components, usePage,
  useForm, persistent layouts, data fetching, state management, and routing.
  Triggers on React component, Inertia page, TypeScript types, form handling, layout,
  or frontend architecture.
---

# React Patterns for Laravel + Inertia.js

## Inertia.js Architecture Overview

Inertia.js bridges Laravel and React without building a separate API. Instead of returning
JSON from controllers, Laravel returns Inertia responses that render React page components
with props derived directly from controller data.

### How It Works

1. **Laravel controller** returns an Inertia response instead of a Blade view:
```php
// app/Http/Controllers/OrderController.php
use Inertia\Inertia;

class OrderController extends Controller
{
    public function index(Request $request): \Inertia\Response
    {
        return Inertia::render('Orders/Index', [
            'orders' => OrderResource::collection(
                Order::query()
                    ->filter($request->only('status', 'search'))
                    ->paginate(15)
            ),
            'filters' => $request->only('status', 'search'),
            'statuses' => OrderStatus::options(),
        ]);
    }
}
```

2. **React page component** receives those props directly:
```tsx
// resources/js/Pages/Orders/Index.tsx
interface Props {
    orders: PaginatedData<Order>
    filters: OrderFilters
    statuses: SelectOption[]
}

export default function Index({ orders, filters, statuses }: Props) {
    // Full access to server data as typed props
}
```

3. **No API endpoints needed** for page data. Props come from the controller, validated
   and shaped by Laravel before reaching the frontend.

4. **Client-side navigation** without full page reloads. Inertia intercepts link clicks,
   makes XHR requests, and swaps page components seamlessly.

### HandleInertiaRequests Middleware

The `HandleInertiaRequests` middleware shares data with every page component. This is
the Inertia equivalent of Blade's `View::share()`.

```php
// app/Http/Middleware/HandleInertiaRequests.php
class HandleInertiaRequests extends Middleware
{
    public function share(Request $request): array
    {
        return array_merge(parent::share($request), [
            'auth' => [
                'user' => $request->user()
                    ? UserResource::make($request->user())
                    : null,
            ],
            'flash' => [
                'success' => fn () => $request->session()->get('success'),
                'error' => fn () => $request->session()->get('error'),
            ],
            'locale' => app()->getLocale(),
            'permissions' => fn () => $request->user()
                ? $request->user()->getAllPermissions()->pluck('name')
                : collect(),
        ]);
    }
}
```

Lazy evaluation with closures (`fn () =>`) ensures shared data is only serialized when
actually accessed on the frontend.

---

## Page Component Pattern

Every route maps to exactly one Inertia page component. Pages are the top-level React
components that receive controller data as props.

### Basic Page Component

```tsx
import { Head, usePage } from '@inertiajs/react'
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout'

interface Props {
    orders: PaginatedData<Order>
    filters: OrderFilters
}

export default function Index({ orders, filters }: Props) {
    return (
        <AuthenticatedLayout>
            <Head title="Orders" />

            <div className="py-12">
                <div className="mx-auto max-w-7xl sm:px-6 lg:px-8">
                    <OrderFiltersBar filters={filters} />
                    <OrderTable orders={orders} />
                    <Pagination links={orders.links} />
                </div>
            </div>
        </AuthenticatedLayout>
    )
}
```

### Page with Create/Edit Form

```tsx
import { Head } from '@inertiajs/react'
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout'
import OrderForm from '@/Components/Orders/OrderForm'

interface Props {
    order?: Order
    customers: SelectOption[]
    products: SelectOption[]
}

export default function CreateEdit({ order, customers, products }: Props) {
    const isEditing = !!order

    return (
        <AuthenticatedLayout>
            <Head title={isEditing ? `Edit Order #${order.id}` : 'Create Order'} />

            <div className="py-12">
                <div className="mx-auto max-w-3xl sm:px-6 lg:px-8">
                    <OrderForm
                        order={order}
                        customers={customers}
                        products={products}
                    />
                </div>
            </div>
        </AuthenticatedLayout>
    )
}
```

### Page with Detail View and Actions

```tsx
import { Head, router } from '@inertiajs/react'
import AuthenticatedLayout from '@/Layouts/AuthenticatedLayout'

interface Props {
    order: Order & { customer: Customer; items: OrderItem[] }
    can: {
        update: boolean
        delete: boolean
        approve: boolean
    }
}

export default function Show({ order, can }: Props) {
    function handleDelete() {
        if (confirm('Are you sure you want to delete this order?')) {
            router.delete(route('orders.destroy', order.id))
        }
    }

    function handleApprove() {
        router.post(route('orders.approve', order.id), {}, {
            preserveScroll: true,
        })
    }

    return (
        <AuthenticatedLayout>
            <Head title={`Order #${order.id}`} />

            <div className="py-12">
                <div className="mx-auto max-w-4xl sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between mb-6">
                        <h1 className="text-2xl font-bold">Order #{order.id}</h1>
                        <div className="flex gap-2">
                            {can.approve && (
                                <Button onClick={handleApprove}>Approve</Button>
                            )}
                            {can.update && (
                                <LinkButton href={route('orders.edit', order.id)}>
                                    Edit
                                </LinkButton>
                            )}
                            {can.delete && (
                                <Button variant="danger" onClick={handleDelete}>
                                    Delete
                                </Button>
                            )}
                        </div>
                    </div>

                    <OrderDetails order={order} />
                    <OrderItemsTable items={order.items} />
                </div>
            </div>
        </AuthenticatedLayout>
    )
}
```

---

## Layout Pattern

Layouts wrap page components and persist across navigations. This prevents remounting
shared UI elements (sidebar, header, audio players, etc.) on every page visit.

### Persistent Layout

The recommended approach uses the `layout` static property on page components:

```tsx
// resources/js/Layouts/AuthenticatedLayout.tsx
import { useState, PropsWithChildren } from 'react'
import { Link, usePage } from '@inertiajs/react'

interface LayoutProps {
    header?: string
}

export default function AuthenticatedLayout({
    header,
    children,
}: PropsWithChildren<LayoutProps>) {
    const { auth } = usePage<SharedProps>().props
    const [sidebarOpen, setSidebarOpen] = useState(false)

    return (
        <div className="min-h-screen bg-gray-100">
            <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            <div className="lg:pl-72">
                <Header
                    user={auth.user}
                    onMenuClick={() => setSidebarOpen(true)}
                />

                {header && (
                    <header className="bg-white shadow">
                        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
                            <h2 className="text-xl font-semibold leading-tight text-gray-800">
                                {header}
                            </h2>
                        </div>
                    </header>
                )}

                <main>{children}</main>

                <Footer />
            </div>
        </div>
    )
}
```

### Guest Layout

For unauthenticated pages (login, register, password reset):

```tsx
// resources/js/Layouts/GuestLayout.tsx
import { PropsWithChildren } from 'react'
import { Link } from '@inertiajs/react'

export default function GuestLayout({ children }: PropsWithChildren) {
    return (
        <div className="flex min-h-screen flex-col items-center bg-gray-100 pt-6 sm:justify-center sm:pt-0">
            <div>
                <Link href="/">
                    <ApplicationLogo className="h-20 w-20 fill-current text-gray-500" />
                </Link>
            </div>

            <div className="mt-6 w-full overflow-hidden bg-white px-6 py-4 shadow-md sm:max-w-md sm:rounded-lg">
                {children}
            </div>
        </div>
    )
}
```

### Sidebar Composition

```tsx
// resources/js/Components/Navigation/Sidebar.tsx
import { Link, usePage } from '@inertiajs/react'

interface NavItem {
    label: string
    href: string
    icon: React.ComponentType<{ className?: string }>
    active?: boolean
    permission?: string
}

const navigation: NavItem[] = [
    { label: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { label: 'Orders', href: '/orders', icon: ShoppingCartIcon },
    { label: 'Customers', href: '/customers', icon: UsersIcon },
    { label: 'Products', href: '/products', icon: CubeIcon },
    { label: 'Reports', href: '/reports', icon: ChartBarIcon, permission: 'view-reports' },
]

export default function Sidebar({ open, onClose }: { open: boolean; onClose: () => void }) {
    const { url, props } = usePage<SharedProps>()
    const permissions = props.permissions

    const filteredNav = navigation.filter(
        item => !item.permission || permissions.includes(item.permission)
    )

    return (
        <nav className="fixed inset-y-0 left-0 z-50 w-72 bg-gray-900">
            <div className="flex h-16 items-center px-6">
                <ApplicationLogo className="h-8 w-auto text-white" />
            </div>
            <ul className="space-y-1 px-3">
                {filteredNav.map(item => (
                    <li key={item.href}>
                        <Link
                            href={item.href}
                            className={cn(
                                'flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium',
                                url.startsWith(item.href)
                                    ? 'bg-gray-800 text-white'
                                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                            )}
                        >
                            <item.icon className="h-5 w-5" />
                            {item.label}
                        </Link>
                    </li>
                ))}
            </ul>
        </nav>
    )
}
```

---

## Form Handling with useForm

Inertia's `useForm` hook manages form state, submission, validation errors, and processing
state in a single unified API.

### Basic Form

```tsx
import { useForm } from '@inertiajs/react'
import { FormEvent } from 'react'

interface OrderFormData {
    customer_id: number | ''
    status: OrderStatus
    notes: string
    items: OrderItemFormData[]
}

export default function OrderForm({ order, customers }: Props) {
    const { data, setData, post, put, processing, errors, reset, isDirty } = useForm<OrderFormData>({
        customer_id: order?.customer_id ?? '',
        status: order?.status ?? 'pending',
        notes: order?.notes ?? '',
        items: order?.items ?? [{ product_id: '', quantity: 1, price: 0 }],
    })

    function handleSubmit(e: FormEvent) {
        e.preventDefault()
        if (order) {
            put(route('orders.update', order.id), {
                onSuccess: () => {
                    // redirect handled by Laravel
                },
            })
        } else {
            post(route('orders.store'), {
                onSuccess: () => reset(),
            })
        }
    }

    return (
        <form onSubmit={handleSubmit} className="space-y-6">
            <div>
                <label htmlFor="customer_id" className="block text-sm font-medium text-gray-700">
                    Customer
                </label>
                <select
                    id="customer_id"
                    value={data.customer_id}
                    onChange={e => setData('customer_id', Number(e.target.value))}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                >
                    <option value="">Select a customer</option>
                    {customers.map(c => (
                        <option key={c.value} value={c.value}>{c.label}</option>
                    ))}
                </select>
                {errors.customer_id && (
                    <p className="mt-1 text-sm text-red-600">{errors.customer_id}</p>
                )}
            </div>

            <div>
                <label htmlFor="notes" className="block text-sm font-medium text-gray-700">
                    Notes
                </label>
                <textarea
                    id="notes"
                    value={data.notes}
                    onChange={e => setData('notes', e.target.value)}
                    rows={3}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm"
                />
                {errors.notes && (
                    <p className="mt-1 text-sm text-red-600">{errors.notes}</p>
                )}
            </div>

            <div className="flex justify-end gap-3">
                <Button type="button" variant="secondary" onClick={() => window.history.back()}>
                    Cancel
                </Button>
                <Button type="submit" disabled={processing || !isDirty}>
                    {processing ? 'Saving...' : order ? 'Update Order' : 'Create Order'}
                </Button>
            </div>
        </form>
    )
}
```

### File Uploads

```tsx
const { data, setData, post, progress } = useForm<{
    title: string
    document: File | null
}>({
    title: '',
    document: null,
})

function handleSubmit(e: FormEvent) {
    e.preventDefault()
    post(route('documents.store'), {
        forceFormData: true, // required for file uploads
    })
}

return (
    <form onSubmit={handleSubmit}>
        <input
            type="file"
            onChange={e => setData('document', e.target.files?.[0] ?? null)}
        />
        {progress && (
            <progress value={progress.percentage} max="100">
                {progress.percentage}%
            </progress>
        )}
    </form>
)
```

### Form Validation Errors from Laravel

Laravel validation errors are automatically mapped to the `errors` object. Nested
errors for arrays use dot notation:

```tsx
// Laravel validation
$request->validate([
    'items.*.product_id' => 'required|exists:products,id',
    'items.*.quantity' => 'required|integer|min:1',
]);

// Access in React
errors['items.0.product_id'] // "The items.0.product_id field is required."
```

### Processing State

```tsx
<Button type="submit" disabled={processing}>
    {processing ? (
        <span className="flex items-center gap-2">
            <Spinner className="h-4 w-4 animate-spin" />
            Saving...
        </span>
    ) : (
        'Save'
    )}
</Button>
```

---

## Navigation with router

The Inertia router handles client-side navigation, form submissions, and partial page
reloads.

### Basic Navigation

```tsx
import { router } from '@inertiajs/react'

// Navigate to a page
router.visit('/orders')

// POST request
router.post('/orders', data)

// PATCH/PUT request
router.patch(`/orders/${id}`, data)

// DELETE request
router.delete(`/orders/${id}`)
```

### Preserve State and Scroll

```tsx
// Preserve scroll position on reload
router.visit('/orders', {
    preserveScroll: true,
})

// Preserve component state (e.g., open dropdowns)
router.visit('/orders', {
    preserveState: true,
})

// Both are commonly used together for filtering
router.get('/orders', { status: 'active', page: 1 }, {
    preserveState: true,
    preserveScroll: true,
    replace: true, // replace browser history entry
})
```

### Partial Reloads

Only reload specific props instead of the entire page:

```tsx
router.reload({
    only: ['orders'], // only refresh the orders prop
    onSuccess: () => {
        console.log('Orders refreshed')
    },
})
```

### Link Component

```tsx
import { Link } from '@inertiajs/react'

<Link
    href={route('orders.show', order.id)}
    className="text-indigo-600 hover:text-indigo-900"
    preserveScroll
>
    View Order #{order.id}
</Link>

// Method links
<Link
    href={route('orders.destroy', order.id)}
    method="delete"
    as="button"
    className="text-red-600"
>
    Delete
</Link>
```

### External Redirects

```tsx
// For external URLs, use window.location
window.location.href = 'https://external-service.com/callback'

// Inertia will handle redirects from Laravel automatically
// In Laravel controller:
return redirect()->away('https://stripe.com/checkout/...');
```

---

## Shared Data (usePage)

Access data shared from `HandleInertiaRequests` middleware on every page.

### Typed Shared Props

```tsx
// resources/js/types/index.d.ts
interface SharedProps {
    auth: {
        user: User | null
    }
    flash: {
        success: string | null
        error: string | null
    }
    locale: string
    permissions: string[]
}
```

### Accessing Shared Data

```tsx
import { usePage } from '@inertiajs/react'

export default function Header() {
    const { auth, flash } = usePage<SharedProps>().props

    return (
        <header>
            {auth.user && (
                <span>Welcome, {auth.user.name}</span>
            )}
            {flash.success && (
                <Alert variant="success">{flash.success}</Alert>
            )}
            {flash.error && (
                <Alert variant="error">{flash.error}</Alert>
            )}
        </header>
    )
}
```

### Flash Messages Pattern

```tsx
// resources/js/Components/FlashMessages.tsx
import { usePage } from '@inertiajs/react'
import { useEffect, useState } from 'react'
import { Transition } from '@headlessui/react'

export default function FlashMessages() {
    const { flash } = usePage<SharedProps>().props
    const [visible, setVisible] = useState(false)

    useEffect(() => {
        if (flash.success || flash.error) {
            setVisible(true)
            const timer = setTimeout(() => setVisible(false), 5000)
            return () => clearTimeout(timer)
        }
    }, [flash])

    return (
        <Transition show={visible}>
            {flash.success && (
                <div className="rounded-md bg-green-50 p-4">
                    <p className="text-sm font-medium text-green-800">{flash.success}</p>
                </div>
            )}
            {flash.error && (
                <div className="rounded-md bg-red-50 p-4">
                    <p className="text-sm font-medium text-red-800">{flash.error}</p>
                </div>
            )}
        </Transition>
    )
}
```

---

## TypeScript Conventions

### Page Props Interfaces

Define an interface for every page component's props:

```tsx
// resources/js/types/models.d.ts
interface User {
    id: number
    name: string
    email: string
    email_verified_at: string | null
    avatar_url: string | null
    created_at: string
    updated_at: string
}

interface Order {
    id: number
    customer_id: number
    status: OrderStatus
    total: number
    notes: string | null
    created_at: string
    updated_at: string
    customer?: Customer
    items?: OrderItem[]
}

type OrderStatus = 'pending' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled'

interface OrderItem {
    id: number
    order_id: number
    product_id: number
    quantity: number
    unit_price: number
    total: number
    product?: Product
}
```

### Global Type Declarations

```tsx
// resources/js/types/global.d.ts
import { PageProps as InertiaPageProps } from '@inertiajs/core'

declare module '@inertiajs/core' {
    interface PageProps extends InertiaPageProps {
        auth: {
            user: User | null
        }
        flash: {
            success: string | null
            error: string | null
        }
        permissions: string[]
    }
}
```

### PaginatedData Generic Type

```tsx
// resources/js/types/pagination.d.ts
interface PaginatedData<T> {
    data: T[]
    links: PaginationLinks
    meta: PaginationMeta
}

interface PaginationLinks {
    first: string | null
    last: string | null
    prev: string | null
    next: string | null
}

interface PaginationMeta {
    current_page: number
    from: number | null
    last_page: number
    links: PaginationLink[]
    path: string
    per_page: number
    to: number | null
    total: number
}

interface PaginationLink {
    url: string | null
    label: string
    active: boolean
}
```

### Ziggy Route Types

```tsx
// resources/js/types/ziggy.d.ts
import { route as ziggyRoute } from 'ziggy-js'

declare global {
    function route(name: string, params?: Record<string, any>, absolute?: boolean): string
    function route(): {
        current: (name?: string) => boolean
    }
}
```

### Select Option and Common UI Types

```tsx
// resources/js/types/ui.d.ts
interface SelectOption {
    value: string | number
    label: string
    disabled?: boolean
}

interface OrderFilters {
    search?: string
    status?: OrderStatus
    customer_id?: number
    date_from?: string
    date_to?: string
    sort_by?: string
    sort_direction?: 'asc' | 'desc'
}

interface BreadcrumbItem {
    label: string
    href?: string
}

interface TableColumn<T> {
    key: keyof T | string
    label: string
    sortable?: boolean
    render?: (item: T) => React.ReactNode
}
```

---

## Custom Hooks

### useFilters

URL query parameter management for filtering and sorting:

```tsx
// resources/js/hooks/useFilters.ts
import { router } from '@inertiajs/react'
import { useState, useCallback } from 'react'
import { useDebouncedCallback } from 'use-debounce'

export function useFilters<T extends Record<string, any>>(
    initialFilters: T,
    routeName: string,
) {
    const [filters, setFiltersState] = useState<T>(initialFilters)

    const applyFilters = useCallback((newFilters: Partial<T>) => {
        const merged = { ...filters, ...newFilters }
        setFiltersState(merged as T)

        router.get(route(routeName), merged as Record<string, any>, {
            preserveState: true,
            preserveScroll: true,
            replace: true,
        })
    }, [filters, routeName])

    const debouncedApply = useDebouncedCallback((newFilters: Partial<T>) => {
        applyFilters(newFilters)
    }, 300)

    const resetFilters = useCallback(() => {
        const empty = Object.fromEntries(
            Object.keys(initialFilters).map(key => [key, ''])
        ) as T
        applyFilters(empty)
    }, [initialFilters, applyFilters])

    return {
        filters,
        setFilter: (key: keyof T, value: T[keyof T]) => {
            if (key === 'search') {
                debouncedApply({ [key]: value } as Partial<T>)
            } else {
                applyFilters({ [key]: value } as Partial<T>)
            }
        },
        resetFilters,
    }
}
```

### useConfirmation

```tsx
// resources/js/hooks/useConfirmation.ts
import { useState, useCallback } from 'react'

interface ConfirmationState {
    isOpen: boolean
    title: string
    message: string
    onConfirm: () => void
}

export function useConfirmation() {
    const [state, setState] = useState<ConfirmationState>({
        isOpen: false,
        title: '',
        message: '',
        onConfirm: () => {},
    })

    const confirm = useCallback((options: {
        title: string
        message: string
        onConfirm: () => void
    }) => {
        setState({ isOpen: true, ...options })
    }, [])

    const close = useCallback(() => {
        setState(prev => ({ ...prev, isOpen: false }))
    }, [])

    const handleConfirm = useCallback(() => {
        state.onConfirm()
        close()
    }, [state.onConfirm, close])

    return { ...state, confirm, close, handleConfirm }
}
```

### useToast

```tsx
// resources/js/hooks/useToast.ts
import { usePage } from '@inertiajs/react'
import { useEffect, useState } from 'react'

interface Toast {
    id: string
    type: 'success' | 'error' | 'info' | 'warning'
    message: string
}

export function useToast() {
    const { flash } = usePage<SharedProps>().props
    const [toasts, setToasts] = useState<Toast[]>([])

    useEffect(() => {
        if (flash.success) {
            addToast('success', flash.success)
        }
        if (flash.error) {
            addToast('error', flash.error)
        }
    }, [flash])

    function addToast(type: Toast['type'], message: string) {
        const id = crypto.randomUUID()
        setToasts(prev => [...prev, { id, type, message }])
        setTimeout(() => removeToast(id), 5000)
    }

    function removeToast(id: string) {
        setToasts(prev => prev.filter(t => t.id !== id))
    }

    return { toasts, addToast, removeToast }
}
```

### useDebouncedSearch

```tsx
// resources/js/hooks/useDebouncedSearch.ts
import { router } from '@inertiajs/react'
import { useState, useEffect, useRef } from 'react'

export function useDebouncedSearch(
    initialValue: string,
    routeName: string,
    delay: number = 300,
) {
    const [search, setSearch] = useState(initialValue)
    const isFirstRender = useRef(true)

    useEffect(() => {
        if (isFirstRender.current) {
            isFirstRender.current = false
            return
        }

        const timer = setTimeout(() => {
            router.get(
                route(routeName),
                { search },
                { preserveState: true, preserveScroll: true, replace: true }
            )
        }, delay)

        return () => clearTimeout(timer)
    }, [search, delay, routeName])

    return { search, setSearch }
}
```

---

## State Management

### When Inertia Shared Data Is Enough

Inertia shared data is appropriate for:
- User authentication state
- Flash messages
- Permissions and roles
- Application-wide settings (locale, theme)
- Navigation items

This data is automatically available on every page with no additional setup.

### When to Use React Context

React Context works well for:
- Theme toggling (dark/light mode)
- Sidebar open/close state across components
- Shopping cart (when persistence is via API)
- Modal and dialog management
- Notification system

```tsx
// resources/js/Contexts/SidebarContext.tsx
import { createContext, useContext, useState, PropsWithChildren } from 'react'

interface SidebarContextType {
    isOpen: boolean
    toggle: () => void
    close: () => void
}

const SidebarContext = createContext<SidebarContextType | undefined>(undefined)

export function SidebarProvider({ children }: PropsWithChildren) {
    const [isOpen, setIsOpen] = useState(false)

    return (
        <SidebarContext.Provider value={{
            isOpen,
            toggle: () => setIsOpen(prev => !prev),
            close: () => setIsOpen(false),
        }}>
            {children}
        </SidebarContext.Provider>
    )
}

export function useSidebar() {
    const context = useContext(SidebarContext)
    if (!context) throw new Error('useSidebar must be used within SidebarProvider')
    return context
}
```

### When to Use Zustand

For complex client-side state that needs to be accessed across deeply nested components
without prop drilling or excessive Context nesting. Zustand is the recommended choice
when you have:
- Complex form builders with drag-and-drop
- Real-time collaboration features
- Spreadsheet-like data grids
- Multi-step workflows with undo/redo

```tsx
// resources/js/stores/useCartStore.ts
import { create } from 'zustand'

interface CartItem {
    product_id: number
    name: string
    price: number
    quantity: number
}

interface CartStore {
    items: CartItem[]
    addItem: (item: Omit<CartItem, 'quantity'>) => void
    removeItem: (productId: number) => void
    updateQuantity: (productId: number, quantity: number) => void
    total: () => number
    clear: () => void
}

export const useCartStore = create<CartStore>((set, get) => ({
    items: [],
    addItem: (item) =>
        set(state => {
            const existing = state.items.find(i => i.product_id === item.product_id)
            if (existing) {
                return {
                    items: state.items.map(i =>
                        i.product_id === item.product_id
                            ? { ...i, quantity: i.quantity + 1 }
                            : i
                    ),
                }
            }
            return { items: [...state.items, { ...item, quantity: 1 }] }
        }),
    removeItem: (productId) =>
        set(state => ({
            items: state.items.filter(i => i.product_id !== productId),
        })),
    updateQuantity: (productId, quantity) =>
        set(state => ({
            items: state.items.map(i =>
                i.product_id === productId ? { ...i, quantity } : i
            ),
        })),
    total: () =>
        get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),
    clear: () => set({ items: [] }),
}))
```

### Avoiding State Duplication with Server Data

Never duplicate server data (Inertia props) into local state unless you need to
transform it for a specific interaction:

```tsx
// BAD: duplicating server state
const [orders, setOrders] = useState(props.orders)
// This creates a stale copy that won't update on navigation

// GOOD: use props directly
export default function Index({ orders }: Props) {
    // orders always reflects the latest server data
    return <OrderTable orders={orders} />
}

// GOOD: derive data from props
export default function Index({ orders }: Props) {
    const activeOrders = useMemo(
        () => orders.data.filter(o => o.status !== 'cancelled'),
        [orders.data]
    )
    return <OrderTable orders={activeOrders} />
}
```

---

## Component Organization

```
resources/js/
├── app.tsx                  # Inertia app initialization
├── ssr.tsx                  # SSR entry point
├── bootstrap.ts             # Axios, Echo setup
├── Pages/                   # Inertia pages (one per route)
│   ├── Auth/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   └── ForgotPassword.tsx
│   ├── Dashboard.tsx
│   ├── Orders/
│   │   ├── Index.tsx
│   │   ├── Show.tsx
│   │   └── CreateEdit.tsx
│   └── Profile/
│       ├── Edit.tsx
│       └── Partials/
│           ├── UpdateProfileForm.tsx
│           └── DeleteUserForm.tsx
├── Layouts/                 # Persistent layouts
│   ├── AuthenticatedLayout.tsx
│   └── GuestLayout.tsx
├── Components/              # Reusable UI components
│   ├── ui/                  # Primitives (Button, Input, Modal)
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Modal.tsx
│   │   ├── Select.tsx
│   │   ├── Table.tsx
│   │   ├── Badge.tsx
│   │   ├── Alert.tsx
│   │   └── Pagination.tsx
│   ├── Orders/              # Domain-specific components
│   │   ├── OrderForm.tsx
│   │   ├── OrderTable.tsx
│   │   ├── OrderStatusBadge.tsx
│   │   └── OrderFiltersBar.tsx
│   ├── Navigation/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   └── Breadcrumbs.tsx
│   └── FlashMessages.tsx
├── hooks/                   # Custom React hooks
│   ├── useFilters.ts
│   ├── useConfirmation.ts
│   ├── useDebounce.ts
│   ├── useToast.ts
│   └── usePermissions.ts
├── lib/                     # Utilities
│   ├── cn.ts                # className merge utility
│   ├── formatDate.ts
│   └── formatCurrency.ts
├── types/                   # TypeScript type definitions
│   ├── index.d.ts           # Shared props, global types
│   ├── models.d.ts          # Model interfaces
│   └── global.d.ts          # Module declarations
└── stores/                  # Zustand stores (when needed)
    └── useCartStore.ts
```

### Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Page components | PascalCase, match route | `Orders/Index.tsx` |
| UI components | PascalCase | `Button.tsx` |
| Hooks | camelCase, `use` prefix | `useFilters.ts` |
| Utilities | camelCase | `formatCurrency.ts` |
| Types | PascalCase interfaces | `Order`, `PaginatedData<T>` |
| Stores | camelCase, `use` prefix | `useCartStore.ts` |

---

## Server-Side Rendering (SSR)

### When to Enable SSR

Enable SSR when:
- SEO is important (public-facing pages, marketing pages)
- First-paint performance is critical
- Social media preview cards need server-rendered content

Skip SSR for:
- Internal admin dashboards
- Applications behind authentication
- Real-time collaborative features

### Setup

```tsx
// resources/js/ssr.tsx
import { createInertiaApp } from '@inertiajs/react'
import createServer from '@inertiajs/react/server'
import ReactDOMServer from 'react-dom/server'
import { route } from 'ziggy-js'

createServer(page =>
    createInertiaApp({
        page,
        render: ReactDOMServer.renderToString,
        resolve: name => {
            const pages = import.meta.glob('./Pages/**/*.tsx', { eager: true })
            return pages[`./Pages/${name}.tsx`]
        },
        setup({ App, props }) {
            // @ts-expect-error Ziggy types
            global.route = (name, params, absolute) =>
                route(name, params, absolute, {
                    ...page.props.ziggy,
                    location: new URL(page.props.ziggy.location),
                })

            return <App {...props} />
        },
    })
)
```

### Hydration Considerations

- Ensure server and client render identical output to avoid hydration mismatches.
- Avoid `Date.now()`, `Math.random()`, or browser-only APIs during initial render.
- Use `useEffect` for client-only logic (it does not run during SSR).
- Test both SSR and client rendering paths.

---

## Performance

### React.memo for Expensive Components

```tsx
import { memo } from 'react'

interface OrderRowProps {
    order: Order
    onSelect: (id: number) => void
}

const OrderRow = memo(function OrderRow({ order, onSelect }: OrderRowProps) {
    return (
        <tr>
            <td>{order.id}</td>
            <td>{order.customer?.name}</td>
            <td><OrderStatusBadge status={order.status} /></td>
            <td>{formatCurrency(order.total)}</td>
            <td>
                <Button size="sm" onClick={() => onSelect(order.id)}>
                    View
                </Button>
            </td>
        </tr>
    )
})

export default OrderRow
```

### useMemo and useCallback

```tsx
export default function Index({ orders, filters }: Props) {
    // Memoize expensive computed values
    const orderStats = useMemo(() => ({
        total: orders.data.length,
        pending: orders.data.filter(o => o.status === 'pending').length,
        revenue: orders.data.reduce((sum, o) => sum + o.total, 0),
    }), [orders.data])

    // Stabilize callbacks passed to child components
    const handleSort = useCallback((column: string) => {
        router.get(route('orders.index'), {
            ...filters,
            sort_by: column,
            sort_direction: filters.sort_by === column && filters.sort_direction === 'asc'
                ? 'desc'
                : 'asc',
        }, {
            preserveState: true,
            preserveScroll: true,
        })
    }, [filters])

    return (
        <div>
            <OrderStatsCards stats={orderStats} />
            <OrderTable orders={orders} onSort={handleSort} />
        </div>
    )
}
```

### Lazy Loading Pages

```tsx
// resources/js/app.tsx
import { createInertiaApp } from '@inertiajs/react'
import { createRoot } from 'react-dom/client'
import { Suspense, lazy } from 'react'

createInertiaApp({
    resolve: name => {
        // Eager load common pages
        const eagerPages = import.meta.glob('./Pages/Dashboard.tsx', { eager: true })
        if (eagerPages[`./Pages/${name}.tsx`]) {
            return eagerPages[`./Pages/${name}.tsx`]
        }

        // Lazy load everything else
        const lazyPages = import.meta.glob('./Pages/**/*.tsx')
        return lazyPages[`./Pages/${name}.tsx`]()
    },
    setup({ el, App, props }) {
        createRoot(el).render(
            <Suspense fallback={<LoadingScreen />}>
                <App {...props} />
            </Suspense>
        )
    },
})
```

### Image Optimization

```tsx
// Use Vite's image optimization
import heroImage from '@/images/hero.jpg?w=800&format=webp'

// Responsive images with srcSet
function ResponsiveImage({ src, alt }: { src: string; alt: string }) {
    return (
        <picture>
            <source srcSet={`${src}?w=400&format=webp 400w, ${src}?w=800&format=webp 800w`} type="image/webp" />
            <img
                src={`${src}?w=800`}
                alt={alt}
                loading="lazy"
                className="h-auto w-full rounded-lg"
            />
        </picture>
    )
}
```

### Bundle Size

- Use dynamic imports for heavy libraries (chart.js, date-fns locales)
- Tree-shake icon libraries (import specific icons, not entire sets)
- Analyze bundle with `npx vite-bundle-visualizer`
- Split vendor chunks in `vite.config.ts`:

```ts
// vite.config.ts
export default defineConfig({
    build: {
        rollupOptions: {
            output: {
                manualChunks: {
                    vendor: ['react', 'react-dom', '@inertiajs/react'],
                    ui: ['@headlessui/react', '@heroicons/react'],
                },
            },
        },
    },
})
```
