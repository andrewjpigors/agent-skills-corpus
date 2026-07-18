---
name: service-provider-architecture
description: >
  Structure Laravel applications using the Service Provider pattern with Model, DTO, Service,
  Controller, FormRequest, Resource, Policy, Event, and Test artifacts. Use when scaffolding a
  new service, creating a Model with business logic, designing DTOs, structuring service classes,
  registering providers, or organizing Laravel code by domain. Triggers on service provider,
  model creation, DTO, service class, controller pattern, form request, or resource controller.
---

# Service Provider Architecture Skill

A comprehensive guide for structuring Laravel applications using the Service Provider pattern. Each domain entity is organized into a consistent set of artifacts — Model, DTO, Service, Controller, FormRequest, Resource, Policy, Event, Listener, and ServiceProvider — ensuring separation of concerns, testability, and maintainability.

**Target users:** Full-stack Laravel + React (Inertia.js) developers who want clean, domain-organized code with predictable patterns.

## Core Principles

1. **Thin controllers** — Controllers only receive requests, delegate to services, and return responses
2. **Fat services** — All business logic lives in service classes, never in controllers or models
3. **Immutable DTOs** — Data moves between layers via typed, readonly data transfer objects
4. **Smart models** — Models define relationships, scopes, casts, and accessors, but no business logic
5. **Explicit authorization** — Every action is authorized via policies, never inline in controllers
6. **Side effects via events** — Notifications, logging, webhooks are decoupled through events/listeners

## Layer Architecture

```
Route (web.php / api.php)
    │
    ▼
Controller ──────────────────────────────────────────────┐
    │                                                     │
    ├──▶ FormRequest (validation + authorization)         │
    │        └── rules(), authorize(), messages()         │
    │                                                     │
    ├──▶ Service (business logic)                         │
    │        ├── Uses Model for data access               │
    │        ├── Uses DTO for data transfer                │
    │        ├── Wraps operations in DB::transaction()     │
    │        └── Dispatches Events for side effects        │
    │                                                     │
    ├──▶ Inertia::render() (for web responses)            │
    │        └── Passes props to React pages              │
    │                                                     │
    ├──▶ Resource (for API responses)                     │
    │        └── toArray() shapes JSON output             │
    │                                                     │
    └──▶ Policy (authorization)                           │
             └── Checked via $this->authorize()           │
                                                          │
Event ◀───────────────────────────────────────────────────┘
    │
    ▼
Listener (side effects: notifications, logging, webhooks)
```

### Request Lifecycle

1. **Route** matches the incoming HTTP request and dispatches to a Controller method
2. **FormRequest** validates and optionally authorizes before the controller body executes
3. **Controller** calls `$this->authorize()` for policy checks, then delegates to a **Service**
4. **Service** performs business logic, uses **Model** for persistence, creates/consumes **DTOs**
5. **Service** dispatches **Events** for side effects
6. **Controller** returns an **Inertia::render()** response (web) or a **Resource** (API)
7. **Listeners** handle events asynchronously (queued) or synchronously

## Directory Structure Convention

```
app/
├── Models/
│   └── Order.php                          # Eloquent model
├── DTOs/
│   └── OrderDTO.php                       # Immutable data transfer object
├── Services/
│   └── OrderService.php                   # Business logic
├── Http/
│   ├── Controllers/
│   │   └── OrderController.php            # Thin resource controller
│   ├── Requests/
│   │   └── Order/
│   │       ├── StoreOrderRequest.php      # Create validation
│   │       └── UpdateOrderRequest.php     # Update validation
│   └── Resources/
│       └── OrderResource.php             # API response transformation
├── Policies/
│   └── OrderPolicy.php                   # Authorization rules
├── Events/
│   └── OrderCreated.php                  # Domain event
├── Listeners/
│   └── SendOrderNotification.php         # Side-effect handler
├── Enums/
│   └── OrderStatus.php                   # Backed enum
├── Exceptions/
│   └── OrderException.php               # Domain exception
└── Providers/
    └── OrderServiceProvider.php          # Wiring: bindings, policies, events

resources/js/
├── Pages/
│   └── Orders/
│       ├── Index.tsx                     # List view
│       ├── Show.tsx                      # Detail view
│       ├── Create.tsx                    # Create form
│       └── Edit.tsx                      # Edit form
├── Components/
│   └── Orders/
│       ├── OrderForm.tsx                 # Shared form component
│       ├── OrderTable.tsx                # Table component
│       └── OrderStatusBadge.tsx          # Status display
└── types/
    └── order.ts                          # TypeScript interfaces

database/
├── migrations/
│   └── 2024_01_01_000000_create_orders_table.php
├── factories/
│   └── OrderFactory.php
└── seeders/
    └── OrderSeeder.php

tests/
├── Feature/
│   └── Http/
│       └── Controllers/
│           └── OrderControllerTest.php
└── Unit/
    ├── Services/
    │   └── OrderServiceTest.php
    └── DTOs/
        └── OrderDTOTest.php
```

## Model Patterns

Models are the **data access layer**. They define the shape of data, how it relates to other data, and how to query it. They must **never** contain business logic.

```php
<?php

namespace App\Models;

use App\Enums\OrderStatus;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\SoftDeletes;
use Illuminate\Database\Eloquent\Casts\Attribute;
use Illuminate\Database\Eloquent\Builder;

class Order extends Model
{
    use HasFactory, SoftDeletes;

    // ──────────────────────────────────────────────
    // Mass assignment protection
    // ──────────────────────────────────────────────
    protected $fillable = [
        'user_id',
        'customer_name',
        'customer_email',
        'status',
        'subtotal',
        'tax',
        'total',
        'notes',
        'shipped_at',
        'delivered_at',
    ];

    // ──────────────────────────────────────────────
    // Attribute casting
    // ──────────────────────────────────────────────
    protected $casts = [
        'status'       => OrderStatus::class,
        'subtotal'     => 'decimal:2',
        'tax'          => 'decimal:2',
        'total'        => 'decimal:2',
        'shipped_at'   => 'datetime',
        'delivered_at' => 'datetime',
    ];

    // ──────────────────────────────────────────────
    // Hidden from serialization
    // ──────────────────────────────────────────────
    protected $hidden = [
        'deleted_at',
    ];

    // ──────────────────────────────────────────────
    // Eager-loaded relationships by default
    // ──────────────────────────────────────────────
    protected $with = [
        'user',
    ];

    // ──────────────────────────────────────────────
    // Relationships
    // ──────────────────────────────────────────────
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function items(): HasMany
    {
        return $this->hasMany(OrderItem::class);
    }

    public function tags(): BelongsToMany
    {
        return $this->belongsToMany(Tag::class)
            ->withPivot('note')
            ->withTimestamps();
    }

    // ──────────────────────────────────────────────
    // Scopes
    // ──────────────────────────────────────────────
    public function scopePending(Builder $query): Builder
    {
        return $query->where('status', OrderStatus::Pending);
    }

    public function scopeForUser(Builder $query, int $userId): Builder
    {
        return $query->where('user_id', $userId);
    }

    public function scopeCreatedBetween(Builder $query, string $from, string $to): Builder
    {
        return $query->whereBetween('created_at', [$from, $to]);
    }

    // ──────────────────────────────────────────────
    // Accessors (Laravel 10+ Attribute syntax)
    // ──────────────────────────────────────────────
    protected function formattedTotal(): Attribute
    {
        return Attribute::make(
            get: fn () => '$' . number_format($this->total, 2),
        );
    }

    protected function isShipped(): Attribute
    {
        return Attribute::make(
            get: fn () => $this->shipped_at !== null,
        );
    }

    // ──────────────────────────────────────────────
    // Model events via boot
    // ──────────────────────────────────────────────
    protected static function boot(): void
    {
        parent::boot();

        static::creating(function (Order $order) {
            $order->status ??= OrderStatus::Pending;
        });
    }
}
```

### Enum for Status

```php
<?php

namespace App\Enums;

enum OrderStatus: string
{
    case Pending    = 'pending';
    case Confirmed  = 'confirmed';
    case Processing = 'processing';
    case Shipped    = 'shipped';
    case Delivered  = 'delivered';
    case Cancelled  = 'cancelled';

    public function label(): string
    {
        return match ($this) {
            self::Pending    => 'Pending',
            self::Confirmed  => 'Confirmed',
            self::Processing => 'Processing',
            self::Shipped    => 'Shipped',
            self::Delivered  => 'Delivered',
            self::Cancelled  => 'Cancelled',
        };
    }

    public function color(): string
    {
        return match ($this) {
            self::Pending    => 'gray',
            self::Confirmed  => 'blue',
            self::Processing => 'yellow',
            self::Shipped    => 'indigo',
            self::Delivered  => 'green',
            self::Cancelled  => 'red',
        };
    }

    /** Statuses that allow cancellation */
    public function isCancellable(): bool
    {
        return in_array($this, [self::Pending, self::Confirmed]);
    }
}
```

See [references/model-patterns.md](references/model-patterns.md) for all 8 relationship types, polymorphic relations, global scopes, observers, and prunable traits.

## DTO Patterns

DTOs are **immutable, typed containers** for moving data between layers. They replace associative arrays with compile-time safety.

```php
<?php

namespace App\DTOs;

use App\Enums\OrderStatus;
use App\Http\Requests\Order\StoreOrderRequest;
use App\Models\Order;
use Carbon\Carbon;

readonly class OrderDTO
{
    public function __construct(
        public string       $customerName,
        public string       $customerEmail,
        public float        $subtotal,
        public float        $tax,
        public float        $total,
        public OrderStatus  $status = OrderStatus::Pending,
        public ?string      $notes = null,
        public ?Carbon      $shippedAt = null,
        public ?int         $id = null,
        public ?int         $userId = null,
    ) {}

    /**
     * Create a DTO from a validated FormRequest.
     */
    public static function fromRequest(StoreOrderRequest $request): self
    {
        return new self(
            customerName:  $request->validated('customer_name'),
            customerEmail: $request->validated('customer_email'),
            subtotal:      (float) $request->validated('subtotal'),
            tax:           (float) $request->validated('tax'),
            total:         (float) $request->validated('total'),
            status:        OrderStatus::from($request->validated('status', 'pending')),
            notes:         $request->validated('notes'),
            userId:        $request->user()->id,
        );
    }

    /**
     * Create a DTO from an Eloquent model.
     */
    public static function fromModel(Order $order): self
    {
        return new self(
            customerName:  $order->customer_name,
            customerEmail: $order->customer_email,
            subtotal:      (float) $order->subtotal,
            tax:           (float) $order->tax,
            total:         (float) $order->total,
            status:        $order->status,
            notes:         $order->notes,
            shippedAt:     $order->shipped_at,
            id:            $order->id,
            userId:        $order->user_id,
        );
    }

    /**
     * Convert to an array suitable for Model::create() or Model::update().
     */
    public function toArray(): array
    {
        return array_filter([
            'user_id'        => $this->userId,
            'customer_name'  => $this->customerName,
            'customer_email' => $this->customerEmail,
            'subtotal'       => $this->subtotal,
            'tax'            => $this->tax,
            'total'          => $this->total,
            'status'         => $this->status->value,
            'notes'          => $this->notes,
            'shipped_at'     => $this->shippedAt,
        ], fn ($value) => $value !== null);
    }
}
```

### Collection DTO

```php
<?php

namespace App\DTOs;

readonly class OrderCollectionDTO
{
    /** @param OrderDTO[] $items */
    public function __construct(
        public array $items,
        public int   $total,
        public int   $perPage,
        public int   $currentPage,
    ) {}

    public static function fromPaginator(\Illuminate\Pagination\LengthAwarePaginator $paginator): self
    {
        return new self(
            items:       collect($paginator->items())->map(fn ($order) => OrderDTO::fromModel($order))->all(),
            total:       $paginator->total(),
            perPage:     $paginator->perPage(),
            currentPage: $paginator->currentPage(),
        );
    }
}
```

See [references/dto-patterns.md](references/dto-patterns.md) for nested DTOs, enum-backed properties, validation within DTOs, spatie/laravel-data integration, and DTO vs Value Object vs FormRequest comparison.

## Service Patterns

Services contain **all business logic**. They coordinate models, DTOs, transactions, and events.

```php
<?php

namespace App\Services;

use App\DTOs\OrderDTO;
use App\Events\OrderCreated;
use App\Events\OrderStatusChanged;
use App\Exceptions\OrderException;
use App\Enums\OrderStatus;
use App\Models\Order;
use Illuminate\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;

class OrderService
{
    public function __construct(
        private readonly NotificationService $notificationService,
    ) {}

    /**
     * List orders with optional filters.
     */
    public function list(array $filters = [], int $perPage = 15): LengthAwarePaginator
    {
        return Order::query()
            ->when($filters['status'] ?? null, fn ($q, $status) => $q->where('status', $status))
            ->when($filters['user_id'] ?? null, fn ($q, $userId) => $q->forUser($userId))
            ->when($filters['search'] ?? null, fn ($q, $search) =>
                $q->where('customer_name', 'like', "%{$search}%")
                  ->orWhere('customer_email', 'like', "%{$search}%")
            )
            ->latest()
            ->paginate($perPage);
    }

    /**
     * Create a new order within a transaction.
     */
    public function create(OrderDTO $dto): Order
    {
        return DB::transaction(function () use ($dto) {
            $order = Order::create($dto->toArray());

            event(new OrderCreated($order));

            return $order->fresh();
        });
    }

    /**
     * Update an existing order.
     */
    public function update(Order $order, OrderDTO $dto): Order
    {
        return DB::transaction(function () use ($order, $dto) {
            $previousStatus = $order->status;

            $order->update($dto->toArray());

            if ($previousStatus !== $dto->status) {
                event(new OrderStatusChanged($order, $previousStatus, $dto->status));
            }

            return $order->fresh();
        });
    }

    /**
     * Delete an order (soft-delete).
     */
    public function delete(Order $order): void
    {
        if (! $order->status->isCancellable()) {
            throw OrderException::cannotDelete($order);
        }

        $order->delete();
    }

    /**
     * Transition order to shipped status.
     */
    public function markAsShipped(Order $order): Order
    {
        if ($order->status !== OrderStatus::Processing) {
            throw OrderException::invalidTransition($order, OrderStatus::Shipped);
        }

        return DB::transaction(function () use ($order) {
            $previousStatus = $order->status;

            $order->update([
                'status'     => OrderStatus::Shipped,
                'shipped_at' => now(),
            ]);

            event(new OrderStatusChanged($order, $previousStatus, OrderStatus::Shipped));

            return $order->fresh();
        });
    }
}
```

### Custom Exception

```php
<?php

namespace App\Exceptions;

use App\Enums\OrderStatus;
use App\Models\Order;
use RuntimeException;

class OrderException extends RuntimeException
{
    public static function cannotDelete(Order $order): self
    {
        return new self(
            "Cannot delete order #{$order->id} — status '{$order->status->label()}' does not allow deletion."
        );
    }

    public static function invalidTransition(Order $order, OrderStatus $target): self
    {
        return new self(
            "Cannot transition order #{$order->id} from '{$order->status->label()}' to '{$target->label()}'."
        );
    }
}
```

See [references/service-patterns.md](references/service-patterns.md) for repository pattern comparison, service composition, action classes, queued operations, and testing patterns.

## Controller Patterns

Controllers are the **HTTP layer**. They are thin — receive requests, delegate to services, return responses.

```php
<?php

namespace App\Http\Controllers;

use App\DTOs\OrderDTO;
use App\Http\Requests\Order\StoreOrderRequest;
use App\Http\Requests\Order\UpdateOrderRequest;
use App\Models\Order;
use App\Services\OrderService;
use Illuminate\Http\RedirectResponse;
use Inertia\Inertia;
use Inertia\Response;

class OrderController extends Controller
{
    public function __construct(
        private readonly OrderService $orderService,
    ) {}

    /**
     * Display a paginated list of orders.
     */
    public function index(): Response
    {
        $orders = $this->orderService->list(
            filters: request()->only(['status', 'search']),
            perPage: 15,
        );

        return Inertia::render('Orders/Index', [
            'orders'  => $orders,
            'filters' => request()->only(['status', 'search']),
        ]);
    }

    /**
     * Show the order creation form.
     */
    public function create(): Response
    {
        return Inertia::render('Orders/Create', [
            'statuses' => \App\Enums\OrderStatus::cases(),
        ]);
    }

    /**
     * Store a new order.
     */
    public function store(StoreOrderRequest $request): RedirectResponse
    {
        $dto   = OrderDTO::fromRequest($request);
        $order = $this->orderService->create($dto);

        return redirect()
            ->route('orders.show', $order)
            ->with('success', 'Order created successfully.');
    }

    /**
     * Display a single order.
     */
    public function show(Order $order): Response
    {
        $this->authorize('view', $order);

        $order->load(['items', 'tags', 'user']);

        return Inertia::render('Orders/Show', [
            'order' => $order,
            'can'   => [
                'edit'   => request()->user()->can('update', $order),
                'delete' => request()->user()->can('delete', $order),
            ],
        ]);
    }

    /**
     * Show the order edit form.
     */
    public function edit(Order $order): Response
    {
        $this->authorize('update', $order);

        return Inertia::render('Orders/Edit', [
            'order'    => $order,
            'statuses' => \App\Enums\OrderStatus::cases(),
        ]);
    }

    /**
     * Update an existing order.
     */
    public function update(UpdateOrderRequest $request, Order $order): RedirectResponse
    {
        $dto = OrderDTO::fromRequest($request);
        $this->orderService->update($order, $dto);

        return redirect()
            ->route('orders.show', $order)
            ->with('success', 'Order updated successfully.');
    }

    /**
     * Delete an order.
     */
    public function destroy(Order $order): RedirectResponse
    {
        $this->authorize('delete', $order);

        $this->orderService->delete($order);

        return redirect()
            ->route('orders.index')
            ->with('success', 'Order deleted successfully.');
    }
}
```

### Route Registration

```php
// routes/web.php
use App\Http\Controllers\OrderController;

Route::middleware(['auth', 'verified'])->group(function () {
    Route::resource('orders', OrderController::class);

    // Custom actions beyond CRUD
    Route::post('orders/{order}/ship', [OrderController::class, 'ship'])
        ->name('orders.ship');
});
```

## FormRequest Patterns

FormRequests handle **all validation** and can also handle authorization. Never validate in controllers.

```php
<?php

namespace App\Http\Requests\Order;

use App\Enums\OrderStatus;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Enum;

class StoreOrderRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return $this->user()->can('create', \App\Models\Order::class);
    }

    /**
     * Get the validation rules.
     */
    public function rules(): array
    {
        return [
            'customer_name'  => ['required', 'string', 'max:255'],
            'customer_email' => ['required', 'email', 'max:255'],
            'subtotal'       => ['required', 'numeric', 'min:0'],
            'tax'            => ['required', 'numeric', 'min:0'],
            'total'          => ['required', 'numeric', 'min:0'],
            'status'         => ['sometimes', new Enum(OrderStatus::class)],
            'notes'          => ['nullable', 'string', 'max:1000'],
            'items'          => ['required', 'array', 'min:1'],
            'items.*.product_id' => ['required', 'exists:products,id'],
            'items.*.quantity'   => ['required', 'integer', 'min:1'],
            'items.*.price'      => ['required', 'numeric', 'min:0'],
        ];
    }

    /**
     * Custom error messages.
     */
    public function messages(): array
    {
        return [
            'items.required' => 'At least one item is required to create an order.',
            'items.min'      => 'At least one item is required to create an order.',
        ];
    }

    /**
     * Prepare data before validation.
     */
    protected function prepareForValidation(): void
    {
        if ($this->has('subtotal') && $this->has('tax')) {
            $this->merge([
                'total' => (float) $this->subtotal + (float) $this->tax,
            ]);
        }
    }
}
```

### Update FormRequest with Conditional Rules

```php
<?php

namespace App\Http\Requests\Order;

use App\Enums\OrderStatus;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;
use Illuminate\Validation\Rules\Enum;

class UpdateOrderRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('update', $this->route('order'));
    }

    public function rules(): array
    {
        return [
            'customer_name'  => ['sometimes', 'string', 'max:255'],
            'customer_email' => ['sometimes', 'email', 'max:255'],
            'subtotal'       => ['sometimes', 'numeric', 'min:0'],
            'tax'            => ['sometimes', 'numeric', 'min:0'],
            'total'          => ['sometimes', 'numeric', 'min:0'],
            'status'         => ['sometimes', new Enum(OrderStatus::class)],
            'notes'          => ['nullable', 'string', 'max:1000'],
        ];
    }
}
```

## Resource Patterns (for API Endpoints)

Resources transform models into JSON responses. Use them for API endpoints, not for Inertia responses (Inertia receives Eloquent models directly).

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class OrderResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id'             => $this->id,
            'customer_name'  => $this->customer_name,
            'customer_email' => $this->customer_email,
            'status'         => $this->status->value,
            'status_label'   => $this->status->label(),
            'status_color'   => $this->status->color(),
            'subtotal'       => $this->subtotal,
            'tax'            => $this->tax,
            'total'          => $this->total,
            'formatted_total'=> $this->formatted_total,
            'notes'          => $this->notes,
            'shipped_at'     => $this->shipped_at?->toISOString(),
            'delivered_at'   => $this->delivered_at?->toISOString(),
            'created_at'     => $this->created_at->toISOString(),
            'updated_at'     => $this->updated_at->toISOString(),

            // Conditional relationships — only included if loaded
            'user'  => UserResource::make($this->whenLoaded('user')),
            'items' => OrderItemResource::collection($this->whenLoaded('items')),
            'tags'  => TagResource::collection($this->whenLoaded('tags')),

            // Conditional attributes
            'can_cancel' => $this->when(
                $request->user() !== null,
                fn () => $request->user()->can('delete', $this->resource),
            ),
        ];
    }
}
```

### Resource Collection with Meta

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;

class OrderCollection extends ResourceCollection
{
    public $collects = OrderResource::class;

    public function toArray($request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total_revenue' => $this->collection->sum('total'),
                'order_count'   => $this->collection->count(),
            ],
        ];
    }
}
```

## Policy Patterns

Policies centralize **all authorization logic**. Every controller action should check a policy gate.

```php
<?php

namespace App\Policies;

use App\Models\Order;
use App\Models\User;

class OrderPolicy
{
    /**
     * Run before any other checks.
     * Returning null falls through to the specific method.
     */
    public function before(User $user, string $ability): ?bool
    {
        if ($user->is_admin) {
            return true;
        }

        return null; // fall through
    }

    /**
     * Determine whether the user can view any orders.
     */
    public function viewAny(User $user): bool
    {
        return true; // All authenticated users can see the list
    }

    /**
     * Determine whether the user can view a specific order.
     */
    public function view(User $user, Order $order): bool
    {
        return $user->id === $order->user_id;
    }

    /**
     * Determine whether the user can create orders.
     */
    public function create(User $user): bool
    {
        return true; // All authenticated users can create
    }

    /**
     * Determine whether the user can update the order.
     */
    public function update(User $user, Order $order): bool
    {
        return $user->id === $order->user_id
            && $order->status->isCancellable();
    }

    /**
     * Determine whether the user can delete the order.
     */
    public function delete(User $user, Order $order): bool
    {
        return $user->id === $order->user_id
            && $order->status->isCancellable();
    }

    /**
     * Determine whether the user can restore a soft-deleted order.
     */
    public function restore(User $user, Order $order): bool
    {
        return $user->id === $order->user_id;
    }

    /**
     * Determine whether the user can permanently delete the order.
     */
    public function forceDelete(User $user, Order $order): bool
    {
        return false; // Never allow permanent deletion via UI
    }
}
```

See [references/policy-patterns.md](references/policy-patterns.md) for team-scoped policies, role-based access with enums, Spatie Permission integration, and passing `can()` to Inertia frontend.

## ServiceProvider Registration

The ServiceProvider wires everything together — bindings, policies, events, and routes.

```php
<?php

namespace App\Providers;

use App\Events\OrderCreated;
use App\Events\OrderStatusChanged;
use App\Listeners\SendOrderNotification;
use App\Listeners\LogOrderStatusChange;
use App\Models\Order;
use App\Policies\OrderPolicy;
use App\Services\OrderService;
use Illuminate\Support\Facades\Event;
use Illuminate\Support\Facades\Gate;
use Illuminate\Support\ServiceProvider;

class OrderServiceProvider extends ServiceProvider
{
    /**
     * Register bindings in the container.
     */
    public function register(): void
    {
        // Bind the service as a singleton (shared instance)
        $this->app->singleton(OrderService::class, function ($app) {
            return new OrderService(
                $app->make(\App\Services\NotificationService::class),
            );
        });
    }

    /**
     * Bootstrap services: policies, events, routes.
     */
    public function boot(): void
    {
        // Register policy
        Gate::policy(Order::class, OrderPolicy::class);

        // Register event listeners
        Event::listen(OrderCreated::class, SendOrderNotification::class);
        Event::listen(OrderStatusChanged::class, LogOrderStatusChange::class);
    }
}
```

### Registering the Provider

Add to `bootstrap/providers.php` (Laravel 11+):

```php
return [
    App\Providers\AppServiceProvider::class,
    App\Providers\OrderServiceProvider::class, // <-- add here
];
```

Or in `config/app.php` (Laravel 10):

```php
'providers' => [
    // ...
    App\Providers\OrderServiceProvider::class,
],
```

## Event / Listener Patterns

Events decouple **side effects** from business logic. The service dispatches events; listeners handle consequences.

### Event Class

```php
<?php

namespace App\Events;

use App\Models\Order;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderCreated
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public readonly Order $order,
    ) {}
}
```

### Status Change Event

```php
<?php

namespace App\Events;

use App\Enums\OrderStatus;
use App\Models\Order;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;

class OrderStatusChanged
{
    use Dispatchable, SerializesModels;

    public function __construct(
        public readonly Order       $order,
        public readonly OrderStatus $previousStatus,
        public readonly OrderStatus $newStatus,
    ) {}
}
```

### Queued Listener

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use App\Notifications\OrderConfirmation;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendOrderNotification implements ShouldQueue
{
    use InteractsWithQueue;

    public function handle(OrderCreated $event): void
    {
        $event->order->user->notify(
            new OrderConfirmation($event->order)
        );
    }

    /**
     * Handle a job failure.
     */
    public function failed(OrderCreated $event, \Throwable $exception): void
    {
        \Log::error('Failed to send order notification', [
            'order_id'  => $event->order->id,
            'exception' => $exception->getMessage(),
        ]);
    }
}
```

### Event Subscriber

```php
<?php

namespace App\Listeners;

use App\Events\OrderCreated;
use App\Events\OrderStatusChanged;
use Illuminate\Events\Dispatcher;

class OrderEventSubscriber
{
    public function handleOrderCreated(OrderCreated $event): void
    {
        // Handle order creation...
    }

    public function handleStatusChanged(OrderStatusChanged $event): void
    {
        // Handle status change...
    }

    public function subscribe(Dispatcher $events): array
    {
        return [
            OrderCreated::class       => 'handleOrderCreated',
            OrderStatusChanged::class => 'handleStatusChanged',
        ];
    }
}
```

## Factory & Seeder Patterns

### Factory with States

```php
<?php

namespace Database\Factories;

use App\Enums\OrderStatus;
use App\Models\Order;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class OrderFactory extends Factory
{
    protected $model = Order::class;

    public function definition(): array
    {
        $subtotal = $this->faker->randomFloat(2, 10, 500);
        $tax      = round($subtotal * 0.1, 2);

        return [
            'user_id'        => User::factory(),
            'customer_name'  => $this->faker->name(),
            'customer_email' => $this->faker->safeEmail(),
            'status'         => OrderStatus::Pending,
            'subtotal'       => $subtotal,
            'tax'            => $tax,
            'total'          => $subtotal + $tax,
            'notes'          => $this->faker->optional()->sentence(),
        ];
    }

    // ── States ──

    public function confirmed(): static
    {
        return $this->state(fn () => ['status' => OrderStatus::Confirmed]);
    }

    public function shipped(): static
    {
        return $this->state(fn () => [
            'status'     => OrderStatus::Shipped,
            'shipped_at' => now()->subDays(rand(1, 5)),
        ]);
    }

    public function delivered(): static
    {
        return $this->state(fn () => [
            'status'       => OrderStatus::Delivered,
            'shipped_at'   => now()->subDays(rand(5, 10)),
            'delivered_at' => now()->subDays(rand(1, 4)),
        ]);
    }

    public function cancelled(): static
    {
        return $this->state(fn () => ['status' => OrderStatus::Cancelled]);
    }

    // ── Relationships ──

    public function withItems(int $count = 3): static
    {
        return $this->has(
            \Database\Factories\OrderItemFactory::new()->count($count),
            'items'
        );
    }
}
```

### Seeder

```php
<?php

namespace Database\Seeders;

use App\Models\Order;
use App\Models\User;
use Illuminate\Database\Seeder;

class OrderSeeder extends Seeder
{
    public function run(): void
    {
        // Create users first (dependency)
        $users = User::factory(10)->create();

        // Create orders for each user
        $users->each(function (User $user) {
            Order::factory()
                ->count(rand(1, 5))
                ->for($user)
                ->withItems()
                ->create();

            // Some shipped orders
            Order::factory()
                ->count(rand(0, 2))
                ->for($user)
                ->shipped()
                ->withItems()
                ->create();
        });
    }
}
```

## TypeScript Interface (Frontend Contract)

```typescript
// resources/js/types/order.ts

export enum OrderStatus {
    Pending    = 'pending',
    Confirmed  = 'confirmed',
    Processing = 'processing',
    Shipped    = 'shipped',
    Delivered  = 'delivered',
    Cancelled  = 'cancelled',
}

export interface Order {
    id: number;
    user_id: number;
    customer_name: string;
    customer_email: string;
    status: OrderStatus;
    subtotal: number;
    tax: number;
    total: number;
    formatted_total: string;
    notes: string | null;
    shipped_at: string | null;
    delivered_at: string | null;
    created_at: string;
    updated_at: string;
    user?: User;
    items?: OrderItem[];
    tags?: Tag[];
}

export interface OrderFilters {
    status?: OrderStatus;
    search?: string;
}

export interface OrderFormData {
    customer_name: string;
    customer_email: string;
    subtotal: number;
    tax: number;
    notes: string;
    items: OrderItemFormData[];
}

export interface OrderPageProps {
    orders: PaginatedData<Order>;
    filters: OrderFilters;
}
```

## Rules Summary Table

| Component | Responsibility | Rule |
|-----------|---------------|------|
| **Controller** | HTTP layer | Thin — only receive request, delegate to service, return response |
| **FormRequest** | Validation | All validation here, never in controller or service |
| **Service** | Business logic | All domain logic, transaction management, event dispatching |
| **DTO** | Data transfer | Immutable, typed, fromRequest/fromModel/toArray |
| **Model** | Data access | Relationships, scopes, casts, accessors — no business logic |
| **Policy** | Authorization | All auth checks — never inline in controllers |
| **Resource** | API transformation | API response shaping only — not for Inertia responses |
| **Event** | Side-effect trigger | Decouple notifications, logging, webhooks from business logic |
| **Listener** | Side-effect handler | Queue-friendly, single-responsibility handlers |
| **ServiceProvider** | Wiring | Container bindings, policy registration, event mapping |
| **Factory** | Test data | Define realistic defaults with composable states |
| **Enum** | Constrained values | Backed enums for status, type, and role fields |

## Anti-Patterns to Avoid

| Anti-Pattern | What's Wrong | Correct Approach |
|-------------|-------------|-----------------|
| Business logic in controller | Untestable, violates SRP | Move to Service class |
| Validation in controller | Duplicated, not reusable | Move to FormRequest |
| Auth checks in controller body | Inconsistent, easy to forget | Use Policy + `$this->authorize()` |
| Raw arrays instead of DTOs | No type safety, no IDE support | Use readonly DTO classes |
| Direct notification in service | Coupling, blocks main flow | Dispatch Event, handle in Listener |
| Fat models with business logic | Violates SRP, hard to test | Model for data, Service for logic |
| `Order::all()` in controllers | N+1, no pagination | Service with `->paginate()` |
| Inline SQL in controllers | Injection risk, hard to maintain | Eloquent scopes in Model |

## Scaffolding Checklist

When creating a new domain entity, create these files in order:

1. [ ] **Enum** — `app/Enums/{Entity}Status.php` (if status/type field exists)
2. [ ] **Migration** — `database/migrations/create_{entities}_table.php`
3. [ ] **Model** — `app/Models/{Entity}.php`
4. [ ] **DTO** — `app/DTOs/{Entity}DTO.php`
5. [ ] **Service** — `app/Services/{Entity}Service.php`
6. [ ] **FormRequests** — `app/Http/Requests/{Entity}/Store{Entity}Request.php` and `Update{Entity}Request.php`
7. [ ] **Controller** — `app/Http/Controllers/{Entity}Controller.php`
8. [ ] **Policy** — `app/Policies/{Entity}Policy.php`
9. [ ] **Resource** — `app/Http/Resources/{Entity}Resource.php` (if API endpoints needed)
10. [ ] **Events** — `app/Events/{Entity}Created.php` (if side effects needed)
11. [ ] **Listeners** — `app/Listeners/...` (for each event)
12. [ ] **ServiceProvider** — `app/Providers/{Entity}ServiceProvider.php`
13. [ ] **Factory** — `database/factories/{Entity}Factory.php`
14. [ ] **Seeder** — `database/seeders/{Entity}Seeder.php`
15. [ ] **Routes** — `routes/web.php` (resource route)
16. [ ] **TypeScript types** — `resources/js/types/{entity}.ts`
17. [ ] **React pages** — `resources/js/Pages/{Entities}/Index.tsx`, `Show.tsx`, `Create.tsx`, `Edit.tsx`
18. [ ] **Tests** — Feature + Unit tests

## Related References

- [Model Patterns](references/model-patterns.md) — Deep Eloquent reference
- [DTO Patterns](references/dto-patterns.md) — Advanced DTO patterns
- [Service Patterns](references/service-patterns.md) — Service class patterns
- [Policy Patterns](references/policy-patterns.md) — Authorization patterns
