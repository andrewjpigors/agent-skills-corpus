---
name: react-native-boost
description: "Use this skill when working on any React Native or Expo project, including project setup, navigation, native modules, platform-specific code, performance optimization, iOS/Android release builds, EAS Build configuration, App Store submission, and Google Play deployment. Trigger when the user mentions React Native, Expo, Metro bundler, native modules, Hermes, EAS, Gradle, Xcode workspace, or cross-platform mobile development."
version: 1.0.0
author: Khalid Abdi
license: MIT
---

# react-native-boost

Complete, current React Native knowledge for AI agents. Targets React Native 0.76+, Expo SDK 52+, React Navigation v7, TanStack Query v5, NativeWind v4, and Zustand v5. Every platform difference is shown with the iOS and Android solution side by side.

## 1. Project Setup and Architecture

### Expo managed versus bare workflow decision tree

Use the Expo managed workflow by default. Move to the bare workflow only when a hard requirement forces it.

```
Do you need a native module with no Expo config plugin and no prebuild support?
  NO  -> Stay managed. Use `npx expo install` and Expo Application Services (EAS) for builds.
  YES -> Can you write an Expo config plugin or use `expo prebuild` to generate native projects?
           YES -> Stay managed with a config plugin. You keep OTA updates and EAS Build.
           NO  -> Go bare. Run `npx expo prebuild` once, commit `ios/` and `android/`, and
                  maintain the native projects by hand from now on.
```

Managed breaks down when you must edit generated native code every build, when a dependency requires a custom `AppDelegate` or `MainActivity` change that no plugin covers, or when you ship a brownfield app embedded in an existing native host. In every other case managed is faster and safer.

### Feature-based folder structure

```
src/
  app/                    # navigation entry, providers, root component
  features/
    auth/
      components/
      hooks/
      screens/
      store/
      api/
      types.ts
      index.ts
    feed/
      components/
      hooks/
      screens/
      store/
      api/
      types.ts
      index.ts
  components/              # shared, feature-agnostic UI
  hooks/                  # shared hooks
  store/                  # global store slices
  lib/                    # api client, mmkv, analytics
  theme/
  utils/
```

Each feature owns its screens, state, and API calls and exports a single public surface from `index.ts`. Cross-feature imports go through `index.ts` only, which keeps boundaries clean.

### tsconfig.json strict mode with path aliases

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "baseUrl": ".",
    "paths": {
      "@components/*": ["src/components/*"],
      "@features/*": ["src/features/*"],
      "@hooks/*": ["src/hooks/*"],
      "@store/*": ["src/store/*"],
      "@lib/*": ["src/lib/*"],
      "@theme/*": ["src/theme/*"]
    }
  },
  "include": ["src", "**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
}
```

The bundler also needs to resolve these aliases. Add `babel-plugin-module-resolver`:

```js
// babel.config.js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      [
        'module-resolver',
        {
          root: ['./src'],
          alias: {
            '@components': './src/components',
            '@features': './src/features',
            '@hooks': './src/hooks',
            '@store': './src/store',
            '@lib': './src/lib',
            '@theme': './src/theme',
          },
        },
      ],
    ],
  };
};
```

### Metro bundler config for monorepos and custom file extensions

```js
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

// Monorepo: watch the whole workspace and resolve hoisted node_modules.
config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];
config.resolver.disableHierarchicalLookup = true;

// Custom file extensions, for example importing .svg as a component or .cjs modules.
config.resolver.sourceExts = [...config.resolver.sourceExts, 'cjs', 'mjs'];
config.resolver.assetExts = config.resolver.assetExts.filter((ext) => ext !== 'svg');
config.resolver.sourceExts.push('svg');

module.exports = config;
```

### .env handling

Two supported approaches. Pick one and stay consistent.

react-native-dotenv, works in managed and bare, reads a `.env` at build time:

```js
// babel.config.js plugins array
[
  'module:react-native-dotenv',
  { moduleName: '@env', path: '.env', safe: true, allowUndefined: false },
]
```

```ts
import { API_URL } from '@env';
```

expo-constants approach, uses `app.config.ts` and `extra`, safer for public values:

```ts
// app.config.ts
export default {
  expo: {
    name: 'MyApp',
    extra: {
      apiUrl: process.env.API_URL ?? 'https://api.example.com',
    },
  },
};
```

```ts
import Constants from 'expo-constants';
const apiUrl = Constants.expoConfig?.extra?.apiUrl as string;
```

Never put secrets in either. Both are readable in the shipped bundle. Keep real secrets on the server.

## 2. Navigation

### React Navigation v7 full setup

Install:

```bash
npx expo install @react-navigation/native @react-navigation/native-stack \
  @react-navigation/bottom-tabs @react-navigation/drawer \
  react-native-screens react-native-safe-area-context react-native-gesture-handler
```

```tsx
// src/app/navigation.tsx
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createDrawerNavigator } from '@react-navigation/drawer';

export type RootStackParamList = {
  Tabs: undefined;
  Details: { itemId: string };
  SettingsModal: undefined;
};

export type TabParamList = {
  Feed: undefined;
  Profile: undefined;
};

const RootStack = createNativeStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();
const Drawer = createDrawerNavigator();

function Tabs() {
  return (
    <Tab.Navigator screenOptions={{ headerShown: true }}>
      <Tab.Screen name="Feed" component={FeedScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

export function RootNavigator() {
  return (
    <NavigationContainer>
      <RootStack.Navigator>
        <RootStack.Group>
          <RootStack.Screen name="Tabs" component={Tabs} options={{ headerShown: false }} />
          <RootStack.Screen name="Details" component={DetailsScreen} />
        </RootStack.Group>
        <RootStack.Group screenOptions={{ presentation: 'modal' }}>
          <RootStack.Screen name="SettingsModal" component={SettingsScreen} />
        </RootStack.Group>
      </RootStack.Navigator>
    </NavigationContainer>
  );
}
```

Modal stacking uses a `RootStack.Group` with `presentation: 'modal'`. A Drawer wraps a stack the same way a Tab navigator does, by nesting the `Drawer.Navigator` at the level you want the drawer to appear.

### Deep linking side by side

Register the URL scheme in `app.json` for managed apps:

```json
{ "expo": { "scheme": "myapp" } }
```

For bare apps, edit both native files. They must match the same scheme.

iOS `ios/MyApp/Info.plist`:

```xml
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>myapp</string>
    </array>
  </dict>
</array>
```

Android `android/app/src/main/AndroidManifest.xml` inside the main `<activity>`:

```xml
<intent-filter android:autoVerify="true">
  <action android:name="android.intent.action.VIEW" />
  <category android:name="android.intent.category.DEFAULT" />
  <category android:name="android.intent.category.BROWSABLE" />
  <data android:scheme="myapp" android:host="app" />
</intent-filter>
```

Wire the prefixes into React Navigation:

```tsx
const linking = {
  prefixes: ['myapp://', 'https://app.example.com'],
  config: {
    screens: {
      Tabs: { screens: { Feed: 'feed', Profile: 'profile' } },
      Details: 'details/:itemId',
    },
  },
};
// <NavigationContainer linking={linking}>
```

### Type-safe navigation

```tsx
import type { NativeStackScreenProps } from '@react-navigation/native-stack';

type Props = NativeStackScreenProps<RootStackParamList, 'Details'>;

export function DetailsScreen({ route, navigation }: Props) {
  const { itemId } = route.params; // typed as string
  return null;
}

// Global type so useNavigation() is typed everywhere.
declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}
```

### Android hardware back button override

```tsx
import { useCallback } from 'react';
import { BackHandler } from 'react-native';
import { useFocusEffect } from '@react-navigation/native';

function useAndroidBack(onBack: () => boolean) {
  useFocusEffect(
    useCallback(() => {
      const sub = BackHandler.addEventListener('hardwareBackPress', onBack);
      return () => sub.remove();
    }, [onBack])
  );
}

// Return true to consume the event and block default back navigation.
useAndroidBack(() => {
  if (isModalOpen) {
    closeModal();
    return true;
  }
  return false;
});
```

`BackHandler` is a no-op on iOS, so this pattern is safe to keep in shared code.

## 3. Platform-Specific Patterns

### Platform.OS, Platform.select, and file extension splitting

```tsx
import { Platform } from 'react-native';

const spacing = Platform.OS === 'ios' ? 12 : 16;

const shadow = Platform.select({
  ios: { shadowColor: '#000', shadowOpacity: 0.2, shadowRadius: 4, shadowOffset: { width: 0, height: 2 } },
  android: { elevation: 4 },
  default: {},
});
```

For larger divergence, split by file extension. Metro picks the right file automatically.

```
Button.ios.tsx      // iOS implementation
Button.android.tsx  // Android implementation
Button.tsx          // fallback for web and other platforms
```

```tsx
import { Button } from './Button'; // resolves per platform, no branching in callers
```

Use `Platform.select` for a handful of values. Use file splitting when the entire component body differs, for example a native iOS blur view versus an Android ripple.

### react-native-safe-area-context

Mount the provider once at the app root, above navigation.

```tsx
import { SafeAreaProvider } from 'react-native-safe-area-context';

export default function App() {
  return (
    <SafeAreaProvider>
      <RootNavigator />
    </SafeAreaProvider>
  );
}
```

```tsx
import { useSafeAreaInsets } from 'react-native-safe-area-context';

function Screen() {
  const insets = useSafeAreaInsets();
  return <View style={{ paddingTop: insets.top, paddingBottom: insets.bottom }} />;
}
```

Prefer `useSafeAreaInsets` with padding over the `SafeAreaView` component when you need per-edge control or a background color that extends into the inset.

### Status bar per-screen control

```tsx
import { StatusBar } from 'expo-status-bar';

// iOS honors barStyle immediately. Android also needs backgroundColor set,
// because the Android status bar has its own solid background.
function DarkScreen() {
  return (
    <>
      <StatusBar style="light" backgroundColor="#111111" />
      {/* screen content */}
    </>
  );
}
```

On iOS the status bar text color follows `style`. On Android you control both the icon color and the bar background color, and a translucent bar requires `translucent` plus top inset padding to avoid content sliding under it.

### KeyboardAvoidingView behavior differences

```tsx
import { KeyboardAvoidingView, Platform } from 'react-native';

<KeyboardAvoidingView
  style={{ flex: 1 }}
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  keyboardVerticalOffset={Platform.OS === 'ios' ? 64 : 0}
>
  {/* form fields */}
</KeyboardAvoidingView>
```

`behavior="padding"` is correct on iOS. On Android the OS already resizes the window via `adjustResize`, so `behavior="height"` (or no behavior with `adjustResize` set) avoids double compensation.

## 4. Native Modules and Permissions

### Bare workflow linking

```bash
# iOS: install pods after adding a native dependency
npx expo install react-native-permissions
cd ios && pod install && cd ..

# Android: autolinking runs during the Gradle build, just rebuild
npx expo run:android
```

If `pod install` reports a version conflict, run `cd ios && pod repo update && pod install`. After changing native dependencies always rebuild the app binary; a Metro reload is not enough.

### react-native-permissions request flow

```ts
import { check, request, RESULTS, PERMISSIONS, openSettings } from 'react-native-permissions';
import { Platform } from 'react-native';

const CAMERA = Platform.select({
  ios: PERMISSIONS.IOS.CAMERA,
  android: PERMISSIONS.ANDROID.CAMERA,
})!;

export async function ensureCamera(): Promise<boolean> {
  const status = await check(CAMERA);
  switch (status) {
    case RESULTS.GRANTED:
      return true;
    case RESULTS.DENIED: {
      // Denied but requestable. Prompt now.
      const next = await request(CAMERA);
      return next === RESULTS.GRANTED;
    }
    case RESULTS.BLOCKED:
      // User selected Do Not Ask Again. Only Settings can change this.
      await openSettings();
      return false;
    case RESULTS.UNAVAILABLE:
      // Feature is not present on this device.
      return false;
    default:
      return false;
  }
}
```

### iOS Info.plist usage description keys

Every one of these is required before the matching API is called, or the app crashes on first use with a purpose-string error at review.

```xml
<key>NSCameraUsageDescription</key>
<string>We use the camera to let you take profile photos.</string>
<key>NSMicrophoneUsageDescription</key>
<string>We use the microphone to record voice notes.</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>We use your location to show nearby results.</string>
<key>NSPhotoLibraryUsageDescription</key>
<string>We access your photo library so you can attach images.</string>
<key>NSContactsUsageDescription</key>
<string>We access your contacts to help you invite friends.</string>
<key>NSCalendarsUsageDescription</key>
<string>We access your calendar to add event reminders.</string>
```

### Android AndroidManifest.xml permission declarations

Declared inside `<manifest>`, above `<application>`. Exact permission strings:

```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.READ_CONTACTS" />
<uses-permission android:name="android.permission.READ_CALENDAR" />
<uses-permission android:name="android.permission.WRITE_CALENDAR" />
```

`READ_MEDIA_IMAGES` replaces `READ_EXTERNAL_STORAGE` for photo access on Android 13 (API 33) and higher.

### Denied and blocked handling without crashing

Never call a native API when the status is `BLOCKED` or `UNAVAILABLE`. Show a short explainer and route the user to Settings:

```ts
if (status === RESULTS.BLOCKED) {
  Alert.alert(
    'Permission needed',
    'Enable camera access in Settings to continue.',
    [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Open Settings', onPress: () => openSettings() },
    ]
  );
}
```

`openSettings()` opens the app settings page on both platforms, so the user can flip the permission and return.

## 5. Performance Optimization

### Hermes engine enablement in the bare workflow

Hermes is on by default in React Native 0.76+. To confirm or force it:

Android `android/app/build.gradle`:

```gradle
project.ext.react = [
    enableHermes: true
]
```

iOS `ios/Podfile`:

```ruby
use_react_native!(
  :path => config[:reactNativePath],
  :hermes_enabled => true
)
```

After changing either flag, run `cd ios && pod install` and rebuild both binaries.

### FlashList migration from FlatList

```bash
npx expo install @shopify/flash-list
```

```tsx
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <Row item={item} />}
  keyExtractor={(item) => item.id}
  estimatedItemSize={72}
/>
```

`estimatedItemSize` should be the average rendered row height in points. Measure one row on device, do not guess wildly, because a bad estimate hurts scroll performance. `keyExtractor` must return a stable unique string; never use the array index, which breaks recycling when the list reorders.

### useMemo and useCallback

```tsx
// Correct: dependency array lists every value read inside.
const sorted = useMemo(() => items.slice().sort(compare), [items]);
const onPress = useCallback(() => select(id), [id]);
```

These hurt performance when misused. A `useMemo` that wraps a cheap expression adds a dependency comparison for no benefit. A `useCallback` whose function is passed to a plain host component that is not memoized just allocates the comparison array with no downstream savings. Reach for them only when the memoized value feeds a `React.memo` child or an expensive computation, and always include a complete dependency array so the value does not go stale.

### react-native-fast-image

```tsx
import FastImage from 'react-native-fast-image';

<FastImage
  style={{ width: 120, height: 120 }}
  source={{
    uri: item.imageUrl,
    priority: FastImage.priority.high,      // low | normal | high
    cache: FastImage.cacheControl.immutable, // immutable | web | cacheOnly
  }}
  resizeMode={FastImage.resizeMode.cover}   // contain | cover | stretch | center
/>
```

Use `immutable` cache for content that never changes at a URL, `web` to respect HTTP cache headers, and `cacheOnly` to read only from disk. Raise `priority` to `high` for above-the-fold images and keep off-screen images at `normal`.

### Bundle analysis

```bash
npx react-native-bundle-visualizer
```

This builds a production bundle and opens a treemap in the browser. Read it from the largest boxes inward. Common wins are a full `lodash` import that should be a per-method import, a moment.js locale bundle you can replace with `date-fns` or `dayjs`, and duplicated copies of a library caused by mismatched versions across a monorepo.

### InteractionManager.runAfterInteractions

```tsx
import { InteractionManager } from 'react-native';

useEffect(() => {
  const task = InteractionManager.runAfterInteractions(() => {
    // Defer expensive work until the navigation animation finishes,
    // so the screen transition stays at 60 frames per second.
    loadHeavyData();
  });
  return () => task.cancel();
}, []);
```

Wrap expensive first-render work, such as building a large chart or parsing a big payload, so the incoming screen animates smoothly and the work runs the moment gestures and transitions settle.

## 6. State Management

### Zustand v5 slices with MMKV persist

```bash
npx expo install zustand react-native-mmkv
```

```ts
// src/store/index.ts
import { create, StateCreator } from 'zustand';
import { persist, createJSONStorage, StateStorage } from 'zustand/middleware';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

const mmkvStorage: StateStorage = {
  setItem: (name, value) => storage.set(name, value),
  getItem: (name) => storage.getString(name) ?? null,
  removeItem: (name) => storage.delete(name),
};

interface AuthSlice {
  token: string | null;
  setToken: (t: string | null) => void;
}
interface UiSlice {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const createAuthSlice: StateCreator<AuthSlice & UiSlice, [], [], AuthSlice> = (set) => ({
  token: null,
  setToken: (token) => set({ token }),
});

const createUiSlice: StateCreator<AuthSlice & UiSlice, [], [], UiSlice> = (set) => ({
  theme: 'light',
  toggleTheme: () => set((s) => ({ theme: s.theme === 'light' ? 'dark' : 'light' })),
});

export const useStore = create<AuthSlice & UiSlice>()(
  persist(
    (...a) => ({ ...createAuthSlice(...a), ...createUiSlice(...a) }),
    {
      name: 'app-store',
      storage: createJSONStorage(() => mmkvStorage),
      partialize: (s) => ({ token: s.token, theme: s.theme }),
    }
  )
);
```

### TanStack Query v5

```bash
npx expo install @tanstack/react-query
```

```tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,        // data is fresh for 60 seconds, no refetch
      gcTime: 5 * 60_000,       // cached data is garbage collected after 5 minutes unused
      retry: 2,
      refetchOnWindowFocus: false, // window focus is not meaningful on native
    },
  },
});

// Wrap the app once.
// <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>

// Prefetch before navigating so the next screen paints instantly.
await queryClient.prefetchQuery({
  queryKey: ['item', id],
  queryFn: () => fetchItem(id),
});
```

`staleTime` controls how long data is considered fresh before a background refetch. `gcTime` controls how long an unused query stays in memory before removal. They are independent: a query can be stale but still cached.

### Context versus Zustand versus TanStack Query

Put server data, anything fetched from an API, in TanStack Query. It handles caching, refetch, and loading states. Put global client state that many screens read and write, such as auth token, theme, or a cart, in Zustand. Use React Context only for low-frequency, rarely-changing dependency injection such as a theme object or a service instance, because every Context value change re-renders all consumers.

### MMKV versus AsyncStorage

MMKV reads and writes synchronously and benchmarks roughly 10 to 30 times faster than AsyncStorage, which is asynchronous and bridge-bound. Migrate on first launch:

```ts
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MMKV } from 'react-native-mmkv';

const storage = new MMKV();

export async function migrateFromAsyncStorage() {
  if (storage.getBoolean('migrated')) return;
  const keys = await AsyncStorage.getAllKeys();
  const entries = await AsyncStorage.multiGet(keys);
  for (const [key, value] of entries) {
    if (value != null) storage.set(key, value);
  }
  storage.set('migrated', true);
}
```

## 7. Styling

### StyleSheet.create versus inline objects

```tsx
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  card: { padding: 16, borderRadius: 12, backgroundColor: '#fff' },
});

// Good: the style object is created once.
<View style={styles.card} />

// Costly: a new object literal is allocated on every render, which defeats
// prop equality checks in memoized children.
<View style={{ padding: 16, borderRadius: 12, backgroundColor: '#fff' }} />
```

Use `StyleSheet.create` for static styles. Only build inline objects when a value is truly dynamic, and even then memoize the object if it feeds a memoized child.

### NativeWind v4

```bash
npx expo install nativewind tailwindcss react-native-reanimated react-native-safe-area-context
```

```js
// tailwind.config.js
module.exports = {
  content: ['./App.tsx', './src/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: { extend: {} },
  plugins: [],
};
```

```js
// babel.config.js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [['babel-preset-expo', { jsxImportSource: 'nativewind' }], 'nativewind/babel'],
  };
};
```

```css
/* global.css, imported once at the app entry */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

```tsx
<View className="p-4 rounded-xl bg-white dark:bg-neutral-900">
  <Text className="text-base font-semibold text-neutral-900 dark:text-white">Hello</Text>
</View>
```

Limitations on React Native versus web: there is no cascade or descendant selector, no pseudo-elements like `::before`, and hover states apply only where a pointer exists. Layout utilities and most color, spacing, and typography classes work across native and web.

### Responsive layouts

```tsx
import { useWindowDimensions, PixelRatio } from 'react-native';

function Card() {
  const { width } = useWindowDimensions();       // updates on rotation and fold
  const fontScale = PixelRatio.getFontScale();    // user font size preference
  const columns = width >= 768 ? 2 : 1;
  const titleSize = 16 * Math.min(fontScale, 1.6); // clamp so layout does not break
  return null;
}
```

`useWindowDimensions` re-renders on orientation and window changes, unlike the static `Dimensions.get`. Multiply base font sizes by `getFontScale` to respect the user's system text size.

### Dynamic Type and font scaling accessibility

```tsx
// Respect system scaling by default. Cap runaway growth on dense UI only.
<Text maxFontSizeMultiplier={1.6}>Balance</Text>

// Never disable scaling app-wide. If you must fix a tiny label, cap it, do not zero it.
<Text allowFontScaling maxFontSizeMultiplier={1.3}>USD</Text>
```

iOS exposes Dynamic Type through the system text size slider and Larger Text setting. Android exposes Font size in Display settings. Both feed `PixelRatio.getFontScale`. Test at the largest setting on both platforms and make sure no text truncates or overlaps.

## 8. Testing

### Jest config for React Native

```js
// jest.config.js
module.exports = {
  preset: 'jest-expo',
  setupFilesAfterEnv: ['@testing-library/react-native/extend-expect', '<rootDir>/jest.setup.ts'],
  transformIgnorePatterns: [
    'node_modules/(?!((jest-)?react-native|@react-native(-community)?|expo(nent)?|@expo(nent)?/.*|@react-navigation/.*|@shopify/flash-list))',
  ],
  moduleNameMapper: {
    '\\.(png|jpg|jpeg|gif|webp|svg)$': '<rootDir>/__mocks__/fileMock.js',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@features/(.*)$': '<rootDir>/src/features/$1',
    '^@hooks/(.*)$': '<rootDir>/src/hooks/$1',
    '^@store/(.*)$': '<rootDir>/src/store/$1',
  },
};
```

```js
// __mocks__/fileMock.js
module.exports = 'test-file-stub';
```

### React Native Testing Library

```tsx
import { render, fireEvent, waitFor, screen } from '@testing-library/react-native';
import { LoginScreen } from '@features/auth/screens/LoginScreen';

test('submits credentials', async () => {
  render(<LoginScreen />);
  fireEvent.changeText(screen.getByPlaceholderText('Email'), 'a@b.com');
  fireEvent.changeText(screen.getByPlaceholderText('Password'), 'secret');
  fireEvent.press(screen.getByText('Sign in'));

  await waitFor(() => {
    expect(screen.getByText('Welcome back')).toBeOnTheScreen();
  });
});
```

### Mocking native modules

```ts
// jest.setup.ts
jest.mock('react-native-permissions', () => require('react-native-permissions/mock'));

jest.mock('react-native-vision-camera', () => ({
  Camera: 'Camera',
  useCameraDevice: () => ({ id: 'back' }),
}));

jest.mock('expo-location', () => ({
  requestForegroundPermissionsAsync: jest.fn().mockResolvedValue({ status: 'granted' }),
  getCurrentPositionAsync: jest.fn().mockResolvedValue({ coords: { latitude: 0, longitude: 0 } }),
}));
```

### Detox for iOS simulator and Android emulator

```js
// .detoxrc.js
module.exports = {
  testRunner: { args: { config: 'e2e/jest.config.js' }, jest: { setupTimeout: 120000 } },
  apps: {
    'ios.release': {
      type: 'ios.app',
      binaryPath: 'ios/build/Build/Products/Release-iphonesimulator/MyApp.app',
      build:
        'xcodebuild -workspace ios/MyApp.xcworkspace -scheme MyApp -configuration Release -sdk iphonesimulator -derivedDataPath ios/build',
    },
    'android.release': {
      type: 'android.apk',
      binaryPath: 'android/app/build/outputs/apk/release/app-release.apk',
      build: 'cd android && ./gradlew assembleRelease assembleAndroidTest -DtestBuildType=release',
    },
  },
  devices: {
    simulator: { type: 'ios.simulator', device: { type: 'iPhone 16 Pro' } },
    emulator: { type: 'android.emulator', device: { avdName: 'Pixel_8_API_34' } },
  },
  configurations: {
    'ios.release': { device: 'simulator', app: 'ios.release' },
    'android.release': { device: 'emulator', app: 'android.release' },
  },
};
```

Build and run:

```bash
detox build --configuration ios.release
detox test --configuration ios.release
detox build --configuration android.release
detox test --configuration android.release
```

### Testing a navigation flow end to end with Detox

```ts
// e2e/login.e2e.ts
import { by, element, expect, device } from 'detox';

describe('login flow', () => {
  beforeAll(async () => {
    await device.launchApp({ newInstance: true });
  });

  it('navigates from login to feed', async () => {
    await element(by.id('email')).typeText('a@b.com');
    await element(by.id('password')).typeText('secret');
    await element(by.id('signIn')).tap();
    await expect(element(by.id('feedScreen'))).toBeVisible();
    await element(by.id('firstItem')).tap();
    await expect(element(by.id('detailsScreen'))).toBeVisible();
  });
});
```

Add `testID` props to the components you target so the selectors stay stable across text changes.

## 9. EAS Build and CI/CD

### eas.json profiles

```json
{
  "cli": { "version": ">= 12.0.0", "appVersionSource": "remote" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal",
      "channel": "preview",
      "ios": { "bundleIdentifier": "com.yourcompany.app.preview" },
      "android": { "buildType": "apk" }
    },
    "production": {
      "channel": "production",
      "autoIncrement": true,
      "android": { "buildType": "app-bundle" }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "you@example.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCDE12345"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

### iOS credentials via EAS

Auto-managed is the default: run `eas build --platform ios` and let EAS create and store the distribution certificate and provisioning profile. For manual provisioning, run `eas credentials` and upload your own `.p12` certificate and `.mobileprovision` profile. Use manual only when your organization requires a specific certificate.

### Android credentials via EAS

```bash
# Let EAS generate and store an upload keystore (recommended).
eas build --platform android
# Inspect or replace it later.
eas credentials
```

EAS generates a keystore on first build and keeps it. Download a backup with `eas credentials`. If you already have a keystore, upload it through the same command so the app signature stays consistent with prior Play Store releases.

### EAS Submit

```bash
eas submit --platform ios --latest --profile production
eas submit --platform android --latest --profile production
```

`--latest` submits the most recent finished build. iOS submission needs `ascAppId` and an Apple team; Android needs a Google Play service account JSON with release permissions.

### GitHub Actions workflow

```yaml
# .github/workflows/build.yml
name: EAS Build
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      - run: eas build --platform all --profile production --non-interactive --no-wait
```

Create the `EXPO_TOKEN` secret from an Expo access token in your account settings.

### expo-updates over-the-air

```bash
npx expo install expo-updates
# Publish an update to a channel already used by an installed build.
eas update --branch production --message "Fix checkout crash"
```

Roll out to a percentage of users:

```bash
eas update:roll-out --branch production --percentage 10
# Raise it after monitoring, or roll back.
eas update:roll-out --branch production --percentage 100
eas channel:rollback --channel production
```

Over-the-air updates ship JavaScript and asset changes only. Any native code or dependency change requires a new store build.

## 10. iOS Release Build without EAS

### Always use .xcworkspace

Open `ios/MyApp.xcworkspace`, never `ios/MyApp.xcodeproj`. CocoaPods installs dependencies into a separate `Pods` project and links them through the workspace. Opening the bare `.xcodeproj` builds without the pods and fails with missing header or missing library errors.

### Release scheme checklist

Product menu, then Scheme, then Edit Scheme. On the Run and Archive tabs confirm:

- Build Configuration is set to Release for Archive.
- The `Debug` only pods and dev menu are excluded from Release.
- `NSAppTransportSecurity` does not allow arbitrary loads in production.
- The correct signing team is selected under Signing and Capabilities.

### Version versus Build

`CFBundleShortVersionString` is the marketing version users see, for example `1.4.0`. `CFBundleVersion` is the build number, for example `1.4.0.42`. Increment the build number on every upload to App Store Connect, even for the same marketing version, because App Store Connect rejects a duplicate build number. Increment the marketing version when you ship user-visible changes.

### Archive and Validate App

Select Any iOS Device as the destination, then Product menu, then Archive. In the Organizer, choose Validate App first. Warning categories mean: missing purpose strings block review, an invalid provisioning profile blocks upload, deprecated API usage is a warning you can usually ship, and a missing `ITSAppUsesNonExemptEncryption` key holds the build for export compliance.

### Distribute App to App Store Connect

In the Organizer choose Distribute App, then App Store Connect, then Upload. Pick automatic signing unless you manage certificates manually. After upload the build appears in App Store Connect under TestFlight in five to fifteen minutes once processing finishes.

### Top 5 Xcode build errors

1. ERROR: `error: No account for team "ABCDE12345". Add a new account in Accounts settings.` FIX: Xcode, Settings, Accounts, add your Apple ID, then reselect the team.
2. ERROR: `error: Signing for "MyApp" requires a development team.` FIX: select a team under Signing and Capabilities for every target including extensions.
3. ERROR: `ld: framework not found Pods_MyApp` FIX: close the project, `cd ios && pod install`, reopen the `.xcworkspace`.
4. ERROR: `Command PhaseScriptExecution failed with a nonzero exit code` FIX: usually a Node path issue in the bundle script; set `NODE_BINARY` in `ios/.xcode.env.local` to the output of `which node`.
5. ERROR: `The sandbox is not in sync with the Podfile.lock` FIX: `cd ios && pod install`, then clean build folder with Shift Command K.

## 11. Android Release Build without EAS

### keytool keystore generation

```bash
keytool -genkey -v -keystore my-release-key.keystore -alias my-key-alias \
  -keyalg RSA -keysize 2048 -validity 10000
```

Store the resulting `.keystore` file outside version control and back it up. Losing it means you can never update the same Play Store listing again.

### signingConfigs reading from local.properties

Never hardcode or commit the passwords. Put them in `android/local.properties`, which is git-ignored:

```
MYAPP_RELEASE_STORE_FILE=my-release-key.keystore
MYAPP_RELEASE_KEY_ALIAS=my-key-alias
MYAPP_RELEASE_STORE_PASSWORD=your_store_password
MYAPP_RELEASE_KEY_PASSWORD=your_key_password
```

`android/app/build.gradle`:

```gradle
def keystoreProps = new Properties()
def keystoreFile = rootProject.file("local.properties")
if (keystoreFile.exists()) {
    keystoreProps.load(new FileInputStream(keystoreFile))
}

android {
    signingConfigs {
        release {
            if (keystoreProps['MYAPP_RELEASE_STORE_FILE']) {
                storeFile file(keystoreProps['MYAPP_RELEASE_STORE_FILE'])
                storePassword keystoreProps['MYAPP_RELEASE_STORE_PASSWORD']
                keyAlias keystoreProps['MYAPP_RELEASE_KEY_ALIAS']
                keyPassword keystoreProps['MYAPP_RELEASE_KEY_PASSWORD']
            }
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro"
        }
    }
}
```

### bundleRelease versus assembleRelease

```bash
# Android App Bundle (AAB) for the Play Store. Google generates per-device APKs.
cd android && ./gradlew bundleRelease
# Output: android/app/build/outputs/bundle/release/app-release.aab

# Universal APK for direct distribution or sideloading.
cd android && ./gradlew assembleRelease
# Output: android/app/build/outputs/apk/release/app-release.apk
```

The Play Store requires an AAB for new apps. Use an APK only for direct install, internal QA, or stores that accept APKs.

### ProGuard and R8 rules

R8 is the default shrinker. Add keep rules in `android/app/proguard-rules.pro`:

```proguard
# Retrofit
-keepattributes Signature, InnerClasses, EnclosingMethod
-keepclassmembers,allowshrinking,allowobfuscation interface * { @retrofit2.http.* <methods>; }
-keep,allowobfuscation,allowshrinking class retrofit2.Response

# Gson
-keepattributes Signature
-keep class com.google.gson.reflect.TypeToken { *; }
-keep class * extends com.google.gson.TypeAdapter

# React Native core
-keep class com.facebook.react.** { *; }
-keep class com.facebook.hermes.** { *; }
-dontwarn com.facebook.react.**

# Firebase
-keep class com.google.firebase.** { *; }
-dontwarn com.google.firebase.**
```

### Top 5 Gradle errors

1. ERROR: `Execution failed for task ':app:mergeDebugResources'` FIX: a duplicate or malformed resource; run `cd android && ./gradlew clean`, then check for two drawables with the same name.
2. ERROR: `Task :app:processDebugGoogleServices FAILED` FIX: `google-services.json` is missing or has the wrong package name; place it in `android/app/` with a `package_name` matching `applicationId`.
3. ERROR: `Could not determine the dependencies of task ':app:compileReleaseJavaWithJavac'` FIX: version mismatch; run `cd android && ./gradlew --refresh-dependencies`.
4. ERROR: `Duplicate class kotlin.collections.jdk8` FIX: force one Kotlin version in `android/build.gradle` with a `resolutionStrategy` on the Kotlin stdlib.
5. ERROR: `SDK location not found` FIX: create `android/local.properties` with `sdk.dir=/Users/you/Library/Android/sdk`.

## 12. App Store Connect Fields

Every field with its exact limit and whether it affects search ranking.

| Field | Limit | Ranked | Notes |
|-------|-------|--------|-------|
| App Name | 30 characters | Yes | Strongest ranking signal, put the top keyword here |
| Subtitle | 30 characters | Yes | Second strongest, no keyword repeats from the name |
| Keywords | 100 characters total, comma separated | Yes | No spaces after commas, no repeats of name or subtitle words |
| Promotional Text | 170 characters | No | Updatable without a new binary or review |
| Description | 4000 characters | No | Not indexed for search, write for conversion |
| What's New | 4000 characters | No | Release notes per version |
| Support URL | Required | No | Must resolve to a real support page |
| Privacy Policy URL | Required for all apps | No | Mandatory since 2018 |
| Marketing URL | Optional | No | Links to your product page |

### Screenshots

Required device sizes for a 2025 submission:

- iPhone 6.9 inch: 1320 x 2868 pixels (portrait).
- iPad Pro 13 inch: 2064 x 2752 pixels (portrait).

Upload the 6.9 inch set and Apple down-scales for smaller iPhones. iPad screenshots are required only if the app supports iPad.

### App Review Information

Provide a demo account and clear notes so review does not reject for inaccessible content.

```
Sign-in required: Yes
Demo username: reviewer@example.com
Demo password: Review2025!
Notes (4000 char limit):
  1. Log in with the demo account above.
  2. The paid features are unlocked on this account, no purchase needed.
  3. Location features: allow the location prompt to see nearby results.
  4. Backend is production, data is safe to interact with.
  Contact: founder@example.com for any blocker during review.
```

### Age rating questionnaire

Answer every category honestly: violence, sexual content, profanity, gambling, and user-generated content. As of July 2025 Apple uses the tiers 4+, 9+, 13+, 16+, and 18+, replacing the older 12+ and 17+ bands. Apps with unrestricted web access or user-generated content are pushed to the higher tiers automatically. An inaccurate answer is grounds for removal after release.

## 13. Google Play Console Fields

| Field | Limit | Notes |
|-------|-------|-------|
| App name | 50 characters | Shown on the listing and in search |
| Short description | 80 characters | Appears above the fold, high impact on install rate |
| Full description | 4000 characters | Indexed by Play search, use natural keywords |

### Content rating

Complete the IARC questionnaire. Categories include violence, sexuality, language, controlled substances, gambling, and interactive elements such as user interaction and shared location. Your answers map to regional ratings automatically: ESRB in the Americas, PEGI in Europe, and USK in Germany. Leaving it incomplete blocks production release.

### Data safety section

Declare every data type your libraries collect. Common React Native mappings:

- react-native-firebase Analytics: collects app interactions and device or other identifiers, linked to the user, used for analytics.
- react-native-analytics (Segment and similar): app interactions and identifiers, used for analytics, often linked to the user.
- Sentry: crash logs and diagnostics, plus device identifiers; declare Crash logs and Diagnostics, not linked to the user unless you attach a user id.
- Crashlytics: Crash logs and Diagnostics, and installation identifiers; declare Diagnostics and Device or other IDs.

If you attach a user id or email to any of these, mark the type as linked to the user.

### Target API level

New apps and updates must target Android 14, API level 34, minimum, enforced since August 2024. Set `targetSdkVersion 34` in `android/build.gradle`. The Play Console rejects an upload that targets a lower level.

### Release tracks

Internal, then Closed, then Open, then Production. Internal testing is nearly instant and limited to 100 testers. Closed testing uses email lists or Google Groups. Open testing is public opt-in. Promote a build up the tracks rather than uploading fresh binaries at each stage.

### Staged rollout

Start Production at a small percentage and widen as signals stay healthy.

- 10 percent: watch the crash-free rate and ANR rate for the first hours.
- 25 percent: confirm no spike in one-star reviews or uninstalls.
- 50 percent: verify server load and any new backend paths hold.
- 100 percent: full release once the above gates pass.

Halt or reduce the rollout in the Play Console immediately if the crash-free rate drops.

## 14. Common Errors Reference

ERROR: Metro has encountered an error: Unable to resolve module
CAUSE: The import path does not match a real file or the package is not installed.
FIX: Verify the path and casing, run `npx expo install <package>`, then restart Metro with a clean cache: `npx expo start --clear`.

ERROR: Invariant Violation: requireNativeComponent was not found
CAUSE: A native module is referenced in JavaScript but not linked into the current build.
FIX: rebuild the binary after installing: `cd ios && pod install && cd ..` then `npx expo run:ios`, or `npx expo run:android`. A Metro reload alone does not link native code.

ERROR: Unable to resolve module X from Y
CAUSE: X is imported from file Y but the dependency is missing or hoisted out of reach in a monorepo.
FIX: install X, and in a monorepo set `config.resolver.nodeModulesPaths` in `metro.config.js` to include the workspace root, then `npx expo start --clear`.

ERROR: ld: library not found for -lX
CAUSE: The iOS linker cannot find a library because pods are out of sync with the Podfile.
FIX: `cd ios && pod install`, open the `.xcworkspace` not the `.xcodeproj`, then clean build folder with Shift Command K.

ERROR: Execution failed for task ':app:mergeDebugResources'
CAUSE: Two Android resources share a name, or a resource file is malformed.
FIX: `cd android && ./gradlew clean`, find the duplicate drawable or string, rename or remove one, then rebuild.

ERROR: Task :app:processDebugGoogleServices FAILED
CAUSE: `google-services.json` is missing or its package name does not match the app `applicationId`.
FIX: download the file from the Firebase console, place it in `android/app/`, and confirm `package_name` equals `applicationId` in `android/app/build.gradle`.

ERROR: error: unknown option '--es-module-specifier-resolution'
CAUSE: A newer Node version dropped a flag a tool passes, usually from a stale Metro or CLI version.
FIX: upgrade the toolchain: `npx expo install --fix`, delete `node_modules` and reinstall, and pin Node to the version in `.nvmrc`.

ERROR: Hermes crash: no source map
CAUSE: A production Hermes crash stack is not symbolicated because the source map was not shipped to the crash reporter.
FIX: generate the map with `npx expo export --dump-sourcemap`, then symbolicate with `npx metro-symbolicate <bundle>.map < stack.txt`, or upload the Hermes source map to your crash reporter during the release build.

## 15. Submission Workflow Summary

Two parallel paths. Follow the column for your platform, and within each, either the manual tools or EAS.

```
iOS                                          Android
1. Increment CFBundleShortVersionString      1. Increment versionName in build.gradle
   and CFBundleVersion.                          and versionCode.
2. Confirm Info.plist purpose strings.       2. Confirm AndroidManifest permissions.
3a. Manual: open .xcworkspace, select        3a. Manual: cd android && ./gradlew
    Any iOS Device, Product > Archive.           bundleRelease.
3b. EAS: eas build --platform ios            3b. EAS: eas build --platform android
    --profile production.                        --profile production.
4a. Manual: Organizer > Validate App >       4a. Manual: upload app-release.aab in the
    Distribute App > App Store Connect.          Play Console to Internal testing.
4b. EAS: eas submit --platform ios           4b. EAS: eas submit --platform android
    --latest --profile production.               --latest --profile production.
5. Fill App Store Connect metadata,          5. Fill Play Console listing, Data safety,
   screenshots, App Review notes.                content rating, target API 34.
6. Submit for review in App Store Connect.   6. Promote Internal > Closed > Open >
                                                 Production with staged rollout.
7. Release manually or automatically         7. Roll out 10% > 25% > 50% > 100%,
   once Approved.                                monitoring crash-free rate at each gate.
```
