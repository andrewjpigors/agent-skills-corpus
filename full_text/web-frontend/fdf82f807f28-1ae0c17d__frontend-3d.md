---
name: frontend-3d
description: Expert 3D web development with React Three Fiber, Three.js, GLSL shaders, GSAP animations, post-processing, and immersive Awwwards-quality experiences
metadata:
  languages: typescript,javascript,glsl
  frameworks: react-three-fiber,three.js,gsap,drei,postprocessing
---

## What I do

I build production-grade immersive 3D web experiences with modern visual effects:

- **React Three Fiber (R3F)**: Declarative 3D scenes in React with full Three.js power
- **Drei**: Helper components for R3F (controls, loaders, helpers, gizmos)
- **Three.js**: Core 3D engine - meshes, materials, lights, cameras, textures
- **GLSL Shaders**: Custom vertex/fragment shaders for liquid effects, distortions, gradients
- **GSAP + ScrollTrigger**: Scroll-driven animations, timeline sequencing, smooth transitions
- **Lenis**: Smooth scroll for premium feel
- **Post-Processing**: Bloom, DOF, chromatic aberration, film grain, vignette
- **Performance**: Draco/Meshopt compression, KTX2 textures, instancing, lazy loading
- **WebGPU**: Next-gen GPU API for complex simulations

## When to use me

- Creating Awwwards-quality immersive websites
- Building 3D product configurators and viewers
- Implementing scroll-driven 3D storytelling
- Creating particle systems and fluid simulations
- Building interactive 3D landing pages
- Loading and optimizing 3D models (GLB/GLTF)
- Implementing custom shader effects
- Adding post-processing cinematic effects
- Creating WebGL/WebGPU visualizations
- Building 3D data visualizations

## Core Stack

### React Three Fiber (R3F)

The dominant library for 3D in React. Declarative syntax wrapping Three.js.

```tsx
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { useRef } from "react";
import * as THREE from "three";

function RotatingBox() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta * 0.5;
      meshRef.current.rotation.y += delta * 0.3;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#00ff88" metalness={0.8} roughness={0.2} />
    </mesh>
  );
}

function Scene() {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 75 }}
      gl={{ antialias: true, alpha: false }}
      dpr={[1, 2]}
    >
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <RotatingBox />
    </Canvas>
  );
}
```

### Drei Helpers

Essential helpers for R3F development:

```tsx
import {
  // Controls
  OrbitControls,
  TrackballControls,
  MapControls,

  // Transform & Gizmos
  TransformControls,
  GizmoHelper,
  GizmoViewport,

  // Loading
  useGLTF,
  useTexture,
  useFBX,
  useProgress,
  Html,
  Loader,

  // Text
  Text,
  Text3D,
  Center,

  // Shapes
  RoundedBox,
  Capsule,
  TorusKnot,

  // Effects
  Float,
  Sparkles,
  Cloud,
  Stars,
  Trail,

  // Environment
  Environment,
  Lightformer,
  ContactShadows,

  // Misc
  PerspectiveCamera,
  OrthographicCamera,
  MeshTransmissionMaterial,
  MeshDistortMaterial,
  MeshWobbleMaterial,
  Outlines,
  Billboard,
  ScreenSpace,
  Preload,
  PerformanceMonitor,
} from "@react-three/drei";
```

### Meshes & Geometry

```tsx
// Primitive geometries
<mesh>
  <boxGeometry args={[width, height, depth]} />
  <sphereGeometry args={[radius, widthSegments, heightSegments]} />
  <cylinderGeometry args={[radiusTop, radiusBottom, height, radialSegments]} />
  <torusGeometry args={[radius, tube, radialSegments, tubularSegments]} />
  <icosahedronGeometry args={[radius, detail]} />
  <planeGeometry args={[width, height, widthSegments, heightSegments]} />
  <coneGeometry args={[radius, height, radialSegments]} />
  <knotGeometry args={[radius, tube, tubularSegments, radialSegments]} />
</mesh>

// Custom geometry from buffer attributes
const vertices = new Float32Array([...]);
const geometry = new THREE.BufferGeometry();
geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));

<mesh geometry={geometry}>
  <meshBasicMaterial color="red" side={THREE.DoubleSide} />
</mesh>
```

### Materials (PBR)

```tsx
// Standard PBR material
<meshStandardMaterial
  color="#ffffff"
  metalness={0.5}
  roughness={0.5}
  map={colorTexture}
  normalMap={normalTexture}
  roughnessMap={roughnessTexture}
  metalnessMap={metalnessTexture}
  aoMap={aoTexture}
  envMapIntensity={1.0}
/>

// Physical material (more features)
<meshPhysicalMaterial
  color="#ffffff"
  metalness={1}
  roughness={0}
  transmission={0.9}      // Glass effect
  thickness={0.5}
  ior={1.5}               // Index of refraction
  clearcoat={1}
  clearcoatRoughness={0}
  sheen={1}
  sheenColor="#ff0000"
/>

// Drei special materials
<MeshTransmissionMaterial
  transmission={1}
  thickness={0.5}
  chromaticAberration={0.06}
  anisotropy={0.1}
  distortion={0.1}
  temporalDistortion={0.1}
/>

<MeshDistortMaterial
  color="#00ff88"
  distort={0.3}
  speed={2}
/>

// Custom shader material
<shaderMaterial
  vertexShader={vertexShader}
  fragmentShader={fragmentShader}
  uniforms={uniforms}
  transparent
  side={THREE.DoubleSide}
/>
```

### Lights & Shadows

```tsx
// Ambient light - uniform illumination
<ambientLight intensity={0.5} color="#ffffff" />

// Directional light - sun-like, supports shadows
<directionalLight
  position={[5, 5, 5]}
  intensity={1}
  castShadow
  shadow-mapSize-width={2048}
  shadow-mapSize-height={2048}
  shadow-camera-far={50}
  shadow-camera-left={-10}
  shadow-camera-right={10}
  shadow-camera-top={10}
  shadow-camera-bottom={-10}
/>

// Point light - light bulb
<pointLight position={[0, 5, 0]} intensity={1} distance={50} decay={2} />

// Spot light - flashlight
<spotLight
  position={[0, 10, 0]}
  angle={0.3}
  penumbra={1}
  intensity={1}
  castShadow
/>

// Rect area light - studio lighting
<rectAreaLight
  width={3}
  height={3}
  intensity={1}
  position={[-2, 0, 5]}
/>

// Shadow receiver
<mesh receiveShadow>
  <planeGeometry args={[100, 100]} />
  <shadowMaterial opacity={0.5} />
</mesh>

// Drei contact shadows (fake soft shadows)
<ContactShadows
  position={[0, -1.5, 0]}
  opacity={0.5}
  scale={10}
  blur={2}
  far={4}
/>
```

### Camera Controls

```tsx
import { OrbitControls, PerspectiveCamera } from "@react-three/drei";

// Orbit controls
<OrbitControls
  enablePan={true}
  enableZoom={true}
  enableRotate={true}
  autoRotate={true}
  autoRotateSpeed={1}
  minDistance={2}
  maxDistance={10}
  minPolarAngle={0}
  maxPolarAngle={Math.PI / 2}
  dampingFactor={0.05}
  enableDamping={true}
/>

// Custom camera
<PerspectiveCamera makeDefault position={[0, 0, 5]} fov={75} />

// Camera animation with useFrame
function CameraAnimation() {
  const { camera } = useThree();

  useFrame((state) => {
    camera.position.x = Math.sin(state.clock.elapsedTime * 0.5) * 5;
    camera.lookAt(0, 0, 0);
  });

  return null;
}
```

### Transformations

```tsx
// Position, rotation, scale
<mesh
  position={[x, y, z]}
  rotation={[rx, ry, rz]}  // Euler angles in radians
  scale={[sx, sy, sz]}
>
  <boxGeometry />
</mesh>

// Quaternion rotation
<mesh quaternion={new THREE.Quaternion().setFromEuler(new THREE.Euler(0, Math.PI/4, 0))}>

// Group transformations
<group position={[0, 0, 0]} rotation={[0, 0, 0]} scale={1}>
  <mesh>...</mesh>
  <mesh>...</mesh>
</group>

// TransformControls (interactive)
<TransformControls mode="translate" size={0.5}>
  <mesh>
    <boxGeometry />
    <meshStandardMaterial />
  </mesh>
</TransformControls>
```

### useFrame Hook (Animation Loop)

```tsx
import { useFrame } from "@react-three/fiber";

function AnimatedMesh() {
  const meshRef = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    // state.clock.elapsedTime - total time
    // state.clock.getDelta() - frame delta
    // state.mouse - normalized mouse position (-1 to 1)
    // state.camera - current camera
    // state.size - canvas size
    // delta - time since last frame

    if (meshRef.current) {
      meshRef.current.rotation.y += delta;
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime) * 0.5;
    }
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry />
      <meshStandardMaterial />
    </mesh>
  );
}
```

### Textures

```tsx
import { useTexture, useCubeTexture, Environment } from "@react-three/drei";

// Single texture
function TexturedMesh() {
  const texture = useTexture("/textures/color.jpg");
  texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(2, 2);

  return (
    <mesh>
      <boxGeometry />
      <meshStandardMaterial map={texture} />
    </mesh>
  );
}

// Multiple textures
function PBRSurface() {
  const [colorMap, normalMap, roughnessMap, metalnessMap, aoMap] = useTexture([
    "/textures/color.jpg",
    "/textures/normal.jpg",
    "/textures/roughness.jpg",
    "/textures/metalness.jpg",
    "/textures/ao.jpg",
  ]);

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        map={colorMap}
        normalMap={normalMap}
        roughnessMap={roughnessMap}
        metalnessMap={metalnessMap}
        aoMap={aoMap}
      />
    </mesh>
  );
}

// Environment map (HDRi)
<Environment preset="city" background />
// presets: apartment, city, dawn, forest, lobby, night, park, studio, sunset, warehouse
```

### Loading Models

```tsx
import { useGLTF, useFBX, useOBJ, Html, useProgress } from "@react-three/drei";
import { Suspense } from "react";

// GLTF/GLB loading
function Model({ url }: { url: string }) {
  const { scene, animations } = useGLTF(url);
  return <primitive object={scene} dispose={null} />;
}

// With animations
function AnimatedModel({ url }: { url: string }) {
  const { scene, animations } = useGLTF(url);
  const { actions } = useAnimations(animations, scene);

  useEffect(() => {
    actions.idle?.play();
  }, [actions]);

  return <primitive object={scene} dispose={null} />;
}

// Loading progress
function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}% loaded</Html>;
}

// Suspense boundary
<Suspense fallback={<Loader />}>
  <Model url="/models/scene.glb" />
  <Environment preset="studio" />
</Suspense>

// Preload models
useGLTF.preload("/models/scene.glb");
```

### Raycasting & Interaction

```tsx
import { useFrame, useThree } from "@react-three/fiber";
import * as THREE from "react-three-fiber";

function InteractiveMesh() {
  const meshRef = useRef<THREE.Mesh>(null);
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);

  return (
    <mesh
      ref={meshRef}
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = "pointer";
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = "auto";
      }}
      onClick={(e) => {
        e.stopPropagation();
        setClicked(!clicked);
      }}
      onPointerMove={(e) => {
        // e.point - world position
        // e.uv - UV coordinates
        // e.face - face normal
      }}
    >
      <boxGeometry />
      <meshStandardMaterial color={clicked ? "red" : hovered ? "hotpink" : "blue"} />
    </mesh>
  );
}

// Raycaster with three.js
function RaycastExample() {
  const { camera, scene } = useThree();
  const raycaster = useRef(new THREE.Raycaster());

  useFrame((state) => {
    raycaster.current.setFromCamera(state.mouse, camera);
    const intersects = raycaster.current.intersectObjects(scene.children);
    // Handle intersects
  });

  return null;
}
```

### Audio & PositionalAudio

```tsx
import { useLoader, useThree } from "@react-three/fiber";
import { AudioListener, AudioLoader, PositionalAudio } from "three";

function Sound() {
  const soundRef = useRef<PositionalAudio>(null);
  const { camera } = useThree();
  const [listener] = useState(() => new AudioListener());
  const buffer = useLoader(AudioLoader, "/audio/sound.mp3");

  useEffect(() => {
    camera.add(listener);
    if (soundRef.current) {
      soundRef.current.setBuffer(buffer);
      soundRef.current.setRefDistance(1);
      soundRef.current.play();
    }
    return () => {
      camera.remove(listener);
    };
  }, [buffer, camera, listener]);

  return (
    <positionalAudio ref={soundRef} args={[listener]} />
  );
}
```

## GSAP Integration

### ScrollTrigger with R3F

```tsx
import { useGSAP } from "@gsap/react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useThree } from "@react-three/fiber";

gsap.registerPlugin(ScrollTrigger);

function ScrollAnimation() {
  const { camera } = useThree();
  const meshRef = useRef<THREE.Mesh>(null);

  useGSAP(() => {
    // Animate camera on scroll
    gsap.to(camera.position, {
      z: 5,
      scrollTrigger: {
        trigger: "#section-1",
        start: "top center",
        end: "bottom center",
        scrub: 1,
      },
    });

    // Animate mesh on scroll
    if (meshRef.current) {
      gsap.to(meshRef.current.rotation, {
        y: Math.PI * 2,
        scrollTrigger: {
          trigger: "#section-2",
          start: "top bottom",
          end: "bottom top",
          scrub: true,
        },
      });
    }
  });

  return (
    <mesh ref={meshRef}>
      <torusKnotGeometry />
      <meshStandardMaterial />
    </mesh>
  );
}
```

### Smooth Scroll with Lenis

```tsx
import { ReactLenis, useLenis } from "lenis/react";

function Layout({ children }: { children: React.ReactNode }) {
  return (
    <ReactLenis
      root
      options={{
        lerp: 0.1,
        duration: 1.2,
        smoothWheel: true,
        wheelMultiplier: 1,
      }}
    >
      {children}
    </ReactLenis>
  );
}

// Hook into scroll
function ScrollComponent() {
  const lenis = useLenis(({ scroll }) => {
    // scroll position
  });

  return <div>...</div>;
}
```

## GLSL Shaders

### Vertex Shader

```glsl
// vertex.glsl
uniform float uTime;
uniform float uFrequency;
uniform float uAmplitude;

varying vec2 vUv;
varying float vElevation;
varying vec3 vNormal;

void main() {
  vUv = uv;
  vNormal = normal;

  vec3 pos = position;

  // Wave effect
  float elevation = sin(pos.x * uFrequency + uTime) * uAmplitude;
  elevation += sin(pos.y * uFrequency * 0.5 + uTime * 0.8) * uAmplitude * 0.5;
  pos.z += elevation;
  vElevation = elevation;

  gl_Position = projectionMatrix * modelViewMatrix * vec4(pos, 1.0);
}
```

### Fragment Shader

```glsl
// fragment.glsl
uniform float uTime;
uniform vec3 uColor;
uniform sampler2D uTexture;

varying vec2 vUv;
varying float vElevation;
varying vec3 vNormal;

void main() {
  // Color based on elevation
  float mixStrength = (vElevation + 0.5) * 0.5;
  vec3 color = mix(uColor, vec3(1.0, 0.0, 0.0), mixStrength);

  // Or texture
  // vec4 texColor = texture2D(uTexture, vUv);
  // color = texColor.rgb;

  gl_FragColor = vec4(color, 1.0);
}
```

### Custom Shader Material in R3F

```tsx
import { shaderMaterial } from "@react-three/drei";
import { extend, useFrame } from "@react-three/fiber";
import * as THREE from "three";

// Create custom material
const WaveMaterial = shaderMaterial(
  {
    uTime: 0,
    uFrequency: 5.0,
    uAmplitude: 0.1,
    uColor: new THREE.Color("#00ff88"),
  },
  vertexShader,
  fragmentShader
);

extend({ WaveMaterial });

function WaveMesh() {
  const materialRef = useRef<any>(null);

  useFrame((state) => {
    if (materialRef.current) {
      materialRef.current.uTime = state.clock.elapsedTime;
    }
  });

  return (
    <mesh>
      <planeGeometry args={[2, 2, 128, 128]} />
      <waveMaterial ref={materialRef} side={THREE.DoubleSide} wireframe />
    </mesh>
  );
}
```

## Post-Processing

```tsx
import {
  EffectComposer,
  Bloom,
  ChromaticAberration,
  DepthOfField,
  Noise,
  Vignette,
  ToneMapping,
  HueSaturation,
  BrightnessContrast,
  GodRays,
  SSR,
  SSAO,
  Outline,
  Pixelation,
  Glitch,
  DotScreen,
} from "@react-three/postprocessing";
import { BlendFunction, KernelSize } from "postprocessing";

function PostProcessing() {
  return (
    <EffectComposer>
      <Bloom
        intensity={1.5}
        luminanceThreshold={0.9}
        luminanceSmoothing={0.025}
        kernelSize={KernelSize.LARGE}
      />
      <ChromaticAberration
        offset={[0.002, 0.002]}
        blendFunction={BlendFunction.NORMAL}
      />
      <DepthOfField
        focusDistance={0.01}
        focalLength={0.02}
        bokehScale={3}
      />
      <Noise opacity={0.05} />
      <Vignette eskil={false} offset={0.1} darkness={1.1} />
      <HueSaturation
        blendFunction={BlendFunction.NORMAL}
        hue={0}
        saturation={0.1}
      />
    </EffectComposer>
  );
}
```

## Performance Optimization

### Compression

```tsx
// Draco compression (geometry)
import { useGLTF } from "@react-three/drei";
import { DracoLoader } from "three/examples/jsm/loaders/DRACOLoader";

useGLTF("/models/scene.glb", true, (loader) => {
  const dracoLoader = new DracoLoader();
  dracoLoader.setDecoderPath("/draco/");
  loader.setDRACOLoader(dracoLoader);
});

// Meshopt compression (better for animated models)
import { MeshoptDecoder } from "three/examples/jsm/libs/meshopt_decoder.module";

useGLTF("/models/scene.glb", true, (loader) => {
  loader.setMeshoptDecoder(MeshoptDecoder);
});
```

### Instancing

```tsx
import { Instances, Instance } from "@react-three/drei";

function InstancedMeshes() {
  return (
    <Instances limit={1000} castShadow receiveShadow>
      <boxGeometry args={[0.1, 0.1, 0.1]} />
      <meshStandardMaterial />

      {Array.from({ length: 1000 }, (_, i) => (
        <Instance
          key={i}
          position={[
            Math.random() * 10 - 5,
            Math.random() * 10 - 5,
            Math.random() * 10 - 5,
          ]}
          rotation={[Math.random() * Math.PI, Math.random() * Math.PI, 0]}
          color={`hsl(${Math.random() * 360}, 70%, 50%)`}
        />
      ))}
    </Instances>
  );
}
```

### Performance Monitor

```tsx
import { PerformanceMonitor } from "@react-three/drei";

function AdaptiveScene() {
  return (
    <Canvas>
      <PerformanceMonitor
        onDecline={() => {
          // Reduce quality
        }}
        onIncline={() => {
          // Increase quality
        }}
      >
        <Scene />
      </PerformanceMonitor>
    </Canvas>
  );
}
```

### Lazy Loading

```tsx
import dynamic from "next/dynamic";

const Scene3D = dynamic(() => import("@/components/three/scene"), {
  ssr: false,
  loading: () => <div>Loading 3D...</div>,
});
```

## Audio Integration

```tsx
import { Audio, AudioListener, AudioLoader, PositionalAudio } from "three";

function BackgroundMusic() {
  const { camera } = useThree();
  const [listener] = useState(() => new AudioListener());
  const sound = useRef<Audio>(null);
  const buffer = useLoader(AudioLoader, "/audio/music.mp3");

  useEffect(() => {
    camera.add(listener);
    if (sound.current) {
      sound.current.setBuffer(buffer);
      sound.current.setLoop(true);
      sound.current.setVolume(0.5);
      sound.current.play();
    }
    return () => {
      camera.remove(listener);
    };
  }, [buffer, camera, listener]);

  return <audio ref={sound} args={[listener]} />;
}

// Positional audio (3D spatial sound)
function SpatialSound({ position }: { position: [number, number, number] }) {
  const soundRef = useRef<PositionalAudio>(null);
  const { camera } = useThree();
  const [listener] = useState(() => new AudioListener());
  const buffer = useLoader(AudioLoader, "/audio/ambient.mp3");

  useEffect(() => {
    camera.add(listener);
    if (soundRef.current) {
      soundRef.current.setBuffer(buffer);
      soundRef.current.setRefDistance(5);
      sound.current.setDistanceModel("exponential");
      soundRef.current.play();
    }
  }, [buffer, camera, listener]);

  return (
    <mesh position={position}>
      <sphereGeometry args={[0.5]} />
      <meshStandardMaterial color="red" />
      <positionalAudio ref={soundRef} args={[listener]} />
    </mesh>
  );
}
```

## Project Structure

```
src/
├── components/
│   ├── three/
│   │   ├── canvas.tsx          # R3F Canvas wrapper
│   │   ├── scene.tsx           # Main scene composition
│   │   ├── lights.tsx          # Lighting setup
│   │   ├── environment.tsx     # HDRi, environment
│   │   ├── effects.tsx         # Post-processing
│   │   ├── camera.tsx          # Camera setup & controls
│   │   ├── models/
│   │   │   ├── model-loader.tsx
│   │   │   └── animated-model.tsx
│   │   ├── meshes/
│   │   │   ├── custom-mesh.tsx
│   │   │   └── instanced-mesh.tsx
│   │   ├── shaders/
│   │   │   ├── vertex.glsl
│   │   │   ├── fragment.glsl
│   │   │   └── wave-material.tsx
│   │   ├── particles/
│   │   │   ├── particles.tsx
│   │   │   └── sparkles.tsx
│   │   ├── helpers/
│   │   │   ├── gizmos.tsx
│   │   │   └── debug.tsx
│   │   └── audio/
│   │       ├── background-music.tsx
│   │       └── spatial-audio.tsx
│   ├── ui/
│   │   ├── loading-screen.tsx
│   │   └── overlay.tsx
│   └── layout/
│       └── scroll-container.tsx
├── hooks/
│   ├── use-scroll-progress.ts
│   ├── use-mouse-position.ts
│   ├── use-device-performance.ts
│   └── use-intersection-observer.ts
├── shaders/
│   ├── vertex/
│   │   ├── wave.glsl
│   │   ├── noise.glsl
│   │   └── particles.glsl
│   └── fragment/
│       ├── hologram.glsl
│       ├── liquid.glsl
│       └── gradient.glsl
├── utils/
│   ├── texture-loader.ts
│   ├── model-optimizer.ts
│   └── shader-utils.ts
├── stores/
│   └── scene-store.ts          # Zustand for 3D state
├── types/
│   └── three.d.ts              # Three.js type extensions
└── public/
    ├── models/
    │   └── scene.glb
    ├── textures/
    │   ├── color.jpg
    │   ├── normal.jpg
    │   └── roughness.jpg
    └── audio/
        └── ambient.mp3
```

## Best Practices

### Performance Rules
- Always use `dpr={[1, 2]}` for responsive pixel ratio
- Compress models with Draco or Meshopt (90% size reduction)
- Use KTX2 for GPU-ready textures
- Implement instancing for repeated objects
- Use `<PerformanceMonitor>` for adaptive quality
- Lazy load 3D scenes with dynamic imports
- Set `dispose={null}` on `<primitive>` to prevent memory leaks
- Use `<Preload all />` to preload assets

### Model Optimization
- Export as GLB (binary GLTF) for smallest size
- Keep polygon count under 100k for mobile
- Use LOD (Level of Detail) for complex scenes
- Bake lighting into textures when possible
- Remove unused materials and textures from Blender

### Shader Guidelines
- Keep shaders simple on mobile (avoid complex loops)
- Use `varying` to pass data from vertex to fragment
- Normalize normals in fragment shader
- Use `precision mediump float` for mobile
- Test on multiple GPUs

### Interaction Patterns
- Use `onPointerOver/Out` for hover effects
- Use `onClick` for selection
- Use `e.stopPropagation()` to prevent event bubbling
- Change cursor with `document.body.style.cursor`
- Use raycasting for complex picking

### Memory Management
- Dispose geometries, materials, textures when unmounting
- Use `useGLTF.dispose()` when no longer needed
- Remove event listeners in cleanup
- Avoid creating objects in `useFrame`
- Reuse vectors and matrices with `useMemo`

## Environment & Background

```tsx
import { Environment, Stars, Sky } from "@react-three/drei";

// HDRi environment
<Environment
  preset="studio"
  background
  blur={0.8}
  resolution={256}
/>

// Custom HDRi
<Environment
  files="/hdris/studio.hdr"
  background
/>

// Stars
<Stars
  radius={100}
  depth={50}
  count={5000}
  factor={4}
  saturation={0}
  fade
  speed={1}
/>

// Sky
<Sky
  distance={450000}
  sunPosition={[0, 1, 0]}
  inclination={0}
  azimuth={0.25}
/>
```

## Tools & Libraries

- **React Three Fiber**: `@react-three/fiber`
- **Drei**: `@react-three/drei`
- **Post-Processing**: `@react-three/postprocessing`
- **GSAP**: `gsap` + `@gsap/react`
- **Lenis**: `lenis`
- **Three.js**: `three`
- **Spline**: `@splinetool/react-spline`
- **Leva**: `leva` (GUI controls)
- **R3F Helpers**: `@react-three/a11y`, `@react-three/test-utils`

## TSL (Three.js Shading Language) - Node-Based Materials

TSL is the future of Three.js materials. It replaces raw GLSL with a composable, type-safe node system that works with both WebGL and WebGPU backends.

### Why TSL over GLSL

- Works with both `WebGLRenderer` and `WebGPURenderer`
- Type-safe and composable shader nodes
- Automatic optimization by the node compiler
- No string manipulation or `onBeforeCompile` hacks
- Built-in functions for common patterns

### TSL Basics

```ts
import * as THREE from 'three/webgpu';
import {
  color, float, vec2, vec3, vec4,
  texture, uv, normal, position,
  time, sin, cos, add, mul, mix,
  Fn, uniform, varying,
  abs, pow, length, dot, normalize,
  oscSine, oscSquare, oscSawtooth, oscTriangle,
  hash, fract,
} from 'three/tsl';

// Create node material
const material = new THREE.MeshStandardNodeMaterial();

// Color from texture multiplied by tint
material.colorNode = texture(myTexture).mul(color(0xff0000));

// Animated emissive
material.emissiveNode = vec3(
  sin(time.mul(2)),
  cos(time.mul(3)),
  sin(time.mul(1.5))
).mul(0.3);

// Position displacement
material.positionNode = positionLocal.add(
  vec3(0, sin(positionLocal.x.mul(5).add(time)).mul(0.1), 0)
);
```

### TSL Math Operations

```ts
import { add, sub, mul, div, negate, abs, floor, ceil, fract,
  sin, cos, tan, asin, acos, atan, pow, exp, log, sqrt,
  min, max, clamp, mix, step, smoothstep, length, distance,
  dot, cross, normalize, reflect, refract, mod } from 'three/tsl';

// All operations are composable nodes
const wave = sin(position.x.mul(5).add(time)).mul(0.1);
const gradient = mix(color(0xff0000), color(0x0000ff), uv().y);
const fresnel = float(1).sub(dot(normalView, vec3(0, 0, 1))).pow(2);
```

### Custom TSL Functions

```ts
import { Fn, float, vec3, sin, time, positionLocal } from 'three/tsl';

// Define reusable function
const myWave = Fn(([position, frequency, amplitude]) => {
  return sin(position.mul(frequency).add(time)).mul(amplitude);
});

// Use in material
const material = new THREE.MeshStandardNodeMaterial();
material.positionNode = positionLocal.add(
  vec3(0, myWave(positionLocal.x, float(5), float(0.1)), 0)
);
```

### TSL Texture Sampling

```ts
import { texture, uv, color, float } from 'three/tsl';

// Basic texture
material.colorNode = texture(myTexture);

// With UV transform
material.colorNode = texture(myTexture, uv().mul(2));

// Texture with color tint
material.colorNode = texture(myTexture).mul(color(0xff8800));

// Animated UV scroll
material.colorNode = texture(myTexture, uv().add(vec2(time.mul(0.1), 0)));

// Texture blending
const blendFactor = float(0.5);
material.colorNode = mix(texture(tex1), texture(tex2), blendFactor);
```

### TSL Conditional Logic

```ts
import { If, select, greaterThan, lessThan, equal } from 'three/tsl';

// Select pattern (branchless)
material.colorNode = select(
  uv().x.greaterThan(0.5),
  color(0xff0000),
  color(0x0000ff)
);

// If/Else block
If(uv().x.greaterThan(0.5), () => {
  // do something
});
```

### TSL Loops

```ts
import { Loop, int, float } from 'three/tsl';

// GPU-compatible loop
const result = Loop({ type: 'float', start: 0, end: 10, condition: '<' }, ({ i }) => {
  // accumulate something
});
```

### TSL Compute Shaders

```ts
import { Fn, instanceIndex, storage, vec4, time } from 'three/tsl';

// Define compute function
const computeUpdate = Fn(() => {
  const position = particlePositions.element(instanceIndex);
  const velocity = particleVelocities.element(instanceIndex);

  position.xyz = position.xyz.add(velocity.mul(time));
});

// Execute on GPU
renderer.compute(computeUpdate().compute(particleCount));
```

## WebGPU Renderer

WebGPU is the next-generation GPU API for the web, replacing WebGL. Three.js supports it via `WebGPURenderer`.

### Basic WebGPU Setup

```ts
import * as THREE from 'three/webgpu';
import { WebGPURenderer } from 'three/webgpu';

// Initialize
const renderer = new WebGPURenderer({ antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

// MUST call init before rendering
await renderer.init();

// Animation loop
renderer.setAnimationLoop(() => {
  renderer.render(scene, camera);
});
```

### WebGPU vs WebGL Decision Matrix

| Feature | WebGPU | WebGL |
|---------|--------|-------|
| Compute Shaders | ✅ Native | ❌ No |
| TSL Materials | ✅ Full | ⚠️ Limited |
| Draw Calls | Lower | Higher |
| GPU Compute | ✅ | ❌ |
| Browser Support | Chrome, Edge, Firefox | All |
| Fallback | WebGL | - |

**Use WebGPU when:** compute shaders, TSL, advanced node materials, GPU simulations
**Use WebGL when:** maximum browser compatibility, simple scenes

### WebGPU Compute Particles (300k+ particles)

```ts
import * as THREE from 'three/webgpu';
import { instancedArray, Fn, instanceIndex, uniform, vec2, float, time } from 'three/tsl';

const particlesCount = 300000;
const particleArray = instancedArray(particlesCount, 'vec2');
const velocityArray = instancedArray(particlesCount, 'vec2');

// Compute shader for particle update
const computeShader = Fn(() => {
  const particle = particleArray.element(instanceIndex);
  const velocity = velocityArray.element(instanceIndex);
  const limit = uniform(vec2(1, 1));

  const position = particle.add(velocity).toVar();

  // Bounce off boundaries
  velocity.x = position.x.abs().greaterThanEqual(limit.x).select(
    velocity.x.negate(), velocity.x
  );
  velocity.y = position.y.abs().greaterThanEqual(limit.y).select(
    velocity.y.negate(), velocity.y
  );

  position.assign(position.min(limit).max(limit.negate()));
  particle.assign(position);
});

const computeNode = computeShader().compute(particlesCount);

// Render particles
const pointsMaterial = new THREE.PointsNodeMaterial();
pointsMaterial.positionNode = particleArray.element(instanceIndex);
pointsMaterial.colorNode = vec3(1, 1, 1);

const points = new THREE.Points(
  new THREE.BufferGeometry(), // minimal geometry
  pointsMaterial
);
points.count = particlesCount;
scene.add(points);

// In render loop
renderer.compute(computeNode);
renderer.render(scene, camera);
```

### WebGPU Texture Generation via Compute

```ts
import { textureStore, Fn, instanceIndex, float, uvec2, vec4, sin } from 'three/tsl';

const width = 512, height = 512;
const storageTexture = new THREE.StorageTexture(width, height);

const computeTexture = Fn(({ storageTexture }) => {
  const posX = instanceIndex.mod(width);
  const posY = instanceIndex.div(width);
  const indexUV = uvec2(posX, posY);

  const x = float(posX).div(50.0);
  const y = float(posY).div(50.0);
  const v = x.sin().add(y.sin()).add(x.add(y).sin());

  textureStore(storageTexture, indexUV, vec4(v.sin(), v.add(Math.PI).sin(), v.add(1.5).sin(), 1))
    .toWriteOnly();
});

renderer.compute(computeTexture({ storageTexture }).compute(width * height));

// Use as material color
material.colorNode = texture(storageTexture);
```

### WebGPU Ping-Pong Texture (Feedback Effects)

```ts
const pingTexture = new THREE.StorageTexture(w, h);
const pongTexture = new THREE.StorageTexture(w, h);
pingTexture.type = THREE.HalfFloatType;
pongTexture.type = THREE.HalfFloatType;

let phase = true;

// Blur compute shader
const blur = Fn(([readTex, uv]) => {
  const c0 = readTex.load(uv.add(ivec2(-1, 1)));
  const c1 = readTex.load(uv.add(ivec2(-1, -1)));
  const c2 = readTex.load(uv.add(ivec2(0, 0)));
  const c3 = readTex.load(uv.add(ivec2(1, -1)));
  const c4 = readTex.load(uv.add(ivec2(1, 1)));
  return c0.add(c1).add(c2).add(c3).add(c4).div(5.0);
});

// In render loop
renderer.compute(phase ? computeToPong : computeToPing);
material.map = phase ? pongTexture : pingTexture;
phase = !phase;
```

## Advanced Particle Systems

### GPU Particles with Compute Shaders (WebGPU)

```ts
import * as THREE from 'three/webgpu';
import { storage, Fn, instanceIndex, uniform, vec3, vec4, float, time, hash } from 'three/tsl';

const nbParticles = 100000;

// Storage buffers
const particlePositions = storage(
  new THREE.StorageInstancedBufferAttribute(nbParticles, 4), 'vec4', nbParticles
);
const particleVelocities = storage(
  new THREE.StorageInstancedBufferAttribute(nbParticles, 4), 'vec4', nbParticles
);

// Initialize particles
const initParticles = Fn(() => {
  const pos = particlePositions.element(instanceIndex);
  pos.xyz = vec3(
    hash(instanceIndex).mul(10).sub(5),
    hash(instanceIndex.add(1000)).mul(10),
    hash(instanceIndex.add(2000)).mul(10).sub(5)
  );
  pos.w = float(1.0); // life
});

renderer.compute(initParticles().compute(nbParticles));

// Update particles each frame
const updateParticles = Fn(() => {
  const pos = particlePositions.element(instanceIndex);
  const vel = particleVelocities.element(instanceIndex);

  // Apply gravity
  vel.y = vel.y.sub(0.001);

  // Update position
  pos.xyz = pos.xyz.add(vel.xyz.mul(0.016));

  // Reset dead particles
  If(pos.y.lessThan(-10), () => {
    pos.y = float(10);
    vel.y = float(0);
  });
});

// Render with instanced mesh
const geometry = new THREE.SphereGeometry(0.02, 8, 8);
const material = new THREE.MeshStandardNodeMaterial();
material.colorNode = particlePositions.element(instanceIndex).y.mul(0.1).clamp(0, 1);

const mesh = new THREE.Mesh(geometry, material);
mesh.count = nbParticles;
mesh.instanceMatrix = new THREE.InstancedBufferAttribute(
  new Float32Array(nbParticles * 16), 16
);
scene.add(mesh);
```

### Sprite-Based Particles (WebGL Compatible)

```ts
import * as THREE from 'three';

const count = 10000;
const geometry = new THREE.BufferGeometry();
const positions = new Float32Array(count * 3);
const colors = new Float32Array(count * 3);
const sizes = new Float32Array(count);

for (let i = 0; i < count; i++) {
  positions[i * 3] = (Math.random() - 0.5) * 100;
  positions[i * 3 + 1] = Math.random() * 100;
  positions[i * 3 + 2] = (Math.random() - 0.5) * 100;

  colors[i * 3] = Math.random();
  colors[i * 3 + 1] = Math.random();
  colors[i * 3 + 2] = Math.random();

  sizes[i] = Math.random() * 5 + 2;
}

geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

const spriteMap = new THREE.TextureLoader().load('/textures/sprites/particle.png');

const material = new THREE.PointsMaterial({
  size: 5,
  map: spriteMap,
  blending: THREE.AdditiveBlending,
  depthTest: false,
  transparent: true,
  vertexColors: true,
  sizeAttenuation: true,
});

const particles = new THREE.Points(geometry, material);
scene.add(particles);
```

### Custom Shader Particles

```ts
// Vertex shader for particles
const particleVertexShader = `
  attribute float size;
  attribute float alpha;
  varying float vAlpha;
  varying vec3 vColor;

  void main() {
    vAlpha = alpha;
    vColor = color;
    vec4 mvPosition = modelViewMatrix * vec4(position, 1.0);
    gl_PointSize = size * (300.0 / -mvPosition.z);
    gl_Position = projectionMatrix * mvPosition;
  }
`;

// Fragment shader for particles
const particleFragmentShader = `
  uniform sampler2D uTexture;
  varying float vAlpha;
  varying vec3 vColor;

  void main() {
    vec4 texColor = texture2D(uTexture, gl_PointCoord);
    gl_FragColor = vec4(vColor, vAlpha) * texColor;
  }
`;
```

## Morph Targets & Skeletal Animation

### Morph Targets (Blend Shapes)

```ts
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
const gltf = await loader.loadAsync('/models/character.glb');

const mesh = gltf.scene.getObjectByName('Character');

// Morph influences (0 = base, 1 = target)
mesh.morphTargetInfluences[0] = 0.5; // smile
mesh.morphTargetInfluences[1] = 0.3; // blink

// Animate morph targets
function animateMorphTargets(time) {
  mesh.morphTargetInfluences[0] = Math.sin(time) * 0.5 + 0.5;
  mesh.morphTargetInfluences[1] = Math.abs(Math.sin(time * 2));
}
```

### Skeletal Animation (AnimationMixer)

```ts
import * as THREE from 'three';

const mixer = new THREE.AnimationMixer(model);

// Play specific clip
const clip = gltf.animations[0];
const action = mixer.clipAction(clip);
action.play();

// Crossfade between animations
function crossfadeTo(newAction, duration = 0.5) {
  const oldAction = currentAction;
  currentAction = newAction;

  oldAction.fadeOut(duration);
  currentAction.reset().fadeIn(duration).play();
}

// In animation loop
function animate(delta) {
  mixer.update(delta);
}
```

### Instanced Morph Targets (1000+ animated objects)

```ts
const mesh = new THREE.InstancedMesh(geometry, material, 1024);
mesh.morphTargetInfluences = dummy.morphTargetInfluences;
mesh.morphTargetDictionary = dummy.morphTargetDictionary;

// Each instance plays animation at different time offset
for (let i = 0; i < 1024; i++) {
  mixer.setTime(time + timeOffsets[i]);
  mesh.setMorphAt(i, dummy);
}
mesh.morphTexture.needsUpdate = true;
```

## Physics Integration

### Rapier (Rust-based, recommended)

```ts
import RAPIER from '@dimforge/rapier3d-compat';

// Initialize
await RAPIER.init();

const world = new RAPIER.World({ x: 0, y: -9.81, z: 0 });

// Create ground
const groundDesc = RAPIER.ColliderDesc.cuboid(50, 0.1, 50);
world.createCollider(groundDesc);

// Create dynamic rigid body
function createPhysicsBody(mesh, mass = 1) {
  const bodyDesc = RAPIER.RigidBodyDesc.dynamic()
    .setTranslation(mesh.position.x, mesh.position.y, mesh.position.z);
  const body = world.createRigidBody(bodyDesc);

  const colliderDesc = RAPIER.ColliderDesc.ball(0.5)
    .setMass(mass)
    .setRestitution(0.7);
  world.createCollider(colliderDesc, body);

  return body;
}

// Sync physics to Three.js
function syncPhysics(bodies) {
  world.step();

  bodies.forEach(({ mesh, body }) => {
    const pos = body.translation();
    const rot = body.rotation();
    mesh.position.set(pos.x, pos.y, pos.z);
    mesh.quaternion.set(rot.x, rot.y, rot.z, rot.w);
  });
}
```

### Rapier Character Controller

```ts
const controller = world.createCharacterController(0.01);

function moveCharacter(body, desiredMovement, dt) {
  controller.computeColliderMovement(
    groundCollider,
    desiredMovement
  );

  const movement = controller.computedMovement();
  const pos = body.translation();
  body.setNextKinematicTranslation({
    x: pos.x + movement.x,
    y: pos.y + movement.y,
    z: pos.z + movement.z,
  });
}
```

### Cannon.js (Lightweight alternative)

```ts
import * as CANNON from 'cannon-es';

const world = new CANNON.World({
  gravity: new CANNON.Vec3(0, -9.82, 0),
});

// Ground
const groundBody = new CANNON.Body({
  type: CANNON.Body.STATIC,
  shape: new CANNON.Plane(),
});
groundBody.quaternion.setFromEuler(-Math.PI / 2, 0, 0);
world.addBody(groundBody);

// Sphere
const sphereBody = new CANNON.Body({
  mass: 5,
  shape: new CANNON.Sphere(1),
  position: new CANNON.Vec3(0, 10, 0),
});
world.addBody(sphereBody);

// Sync
function updatePhysics(dt) {
  world.step(1 / 60, dt, 3);
  mesh.position.copy(sphereBody.position);
  mesh.quaternion.copy(sphereBody.quaternion);
}
```

## WebXR (VR/AR)

### Basic VR Setup

```ts
import * as THREE from 'three';
import { VRButton } from 'three/addons/webxr/VRButton.js';

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.xr.enabled = true;

document.body.appendChild(VRButton.createButton(renderer));

// Animation loop (automatically handles VR frame timing)
renderer.setAnimationLoop(() => {
  renderer.render(scene, camera);
});
```

### VR Controllers with Hand Tracking

```ts
import { VRButton } from 'three/addons/webxr/VRButton.js';
import { XRControllerModelFactory } from 'three/addons/webxr/XRControllerModelFactory.js';
import { XRHandModelFactory } from 'three/addons/webxr/XRHandModelFactory.js';

renderer.xr.enabled = true;

// Controllers
const controller1 = renderer.xr.getController(0);
scene.add(controller1);

const controller2 = renderer.xr.getController(1);
scene.add(controller2);

// Controller models (visual)
const controllerModelFactory = new XRControllerModelFactory();

const controllerGrip1 = renderer.xr.getControllerGrip(0);
controllerGrip1.add(controllerModelFactory.createControllerModel(controllerGrip1));
scene.add(controllerGrip1);

// Hand models
const handModelFactory = new XRHandModelFactory();

const hand1 = renderer.xr.getHand(0);
hand1.add(handModelFactory.createHandModel(hand1));
scene.add(hand1);

// Enable hand tracking
const sessionInit = { requiredFeatures: ['hand-tracking'] };
document.body.appendChild(VRButton.createButton(renderer, sessionInit));
```

### AR Setup with Hit Test

```ts
import { ARButton } from 'three/addons/webxr/ARButton.js';

renderer.xr.enabled = true;

const sessionInit = {
  requiredFeatures: ['hit-test'],
  optionalFeatures: ['dom-overlay'],
};

document.body.appendChild(ARButton.createButton(renderer, sessionInit));

// Hit test for placing objects
let hitTestSource = null;

renderer.xr.addEventListener('sessionstart', async () => {
  const session = renderer.xr.getSession();
  const viewerSpace = await session.requestReferenceSpace('viewer');
  hitTestSource = await session.requestHitTestSource({ space: viewerSpace });
});

// On select, place object at hit point
controller1.addEventListener('select', () => {
  if (hitTestSource) {
    const frame = renderer.xr.getFrame();
    const hitTestResults = frame.getHitTestResults(hitTestSource);

    if (hitTestResults.length > 0) {
      const hit = hitTestResults[0];
      const pose = hit.getPose(referenceSpace);

      // Place object
      const mesh = new THREE.Mesh(geometry, material);
      mesh.position.fromArray(pose.transform.position);
      mesh.quaternion.fromArray(pose.transform.orientation);
      scene.add(mesh);
    }
  }
});
```

## Advanced Effects

### Water Reflection/Refraction

```ts
import { Water } from 'three/addons/objects/Water.js';

const waterGeometry = new THREE.PlaneGeometry(100, 100);

const water = new Water(waterGeometry, {
  textureWidth: 512,
  textureHeight: 512,
  waterNormals: new THREE.TextureLoader().load('/textures/waternormals.jpg', (texture) => {
    texture.wrapS = texture.wrapT = THREE.RepeatWrapping;
  }),
  sunDirection: new THREE.Vector3(),
  sunColor: 0xffffff,
  waterColor: 0x001e0f,
  distortionScale: 3.7,
  fog: scene.fog !== undefined,
});

water.rotation.x = -Math.PI / 2;
scene.add(water);

// Animate water
function animate() {
  water.material.uniforms['time'].value += 1.0 / 60.0;
}
```

### Sky Dome

```ts
import { Sky } from 'three/addons/objects/Sky.js';

const sky = new Sky();
sky.scale.setScalar(10000);
scene.add(sky);

const skyUniforms = sky.material.uniforms;
skyUniforms['turbidity'].value = 10;
skyUniforms['rayleigh'].value = 2;
skyUniforms['mieCoefficient'].value = 0.005;
skyUniforms['mieDirectionalG'].value = 0.8;

// Update sun position
const sun = new THREE.Vector3();
const phi = THREE.MathUtils.degToRad(90 - elevation);
const theta = THREE.MathUtils.degToRad(azimuth);
sun.setFromSphericalCoords(1, phi, theta);
skyUniforms['sunPosition'].value.copy(sun);
```

### Volumetric Fog/Smoke (WebGPU)

```ts
import * as THREE from 'three/webgpu';
import { VolumeNodeMaterial } from 'three/webgpu';
import { Fn, texture3D, time, vec3, uniform, screenCoordinate } from 'three/tsl';
import { bayer16 } from 'three/addons/tsl/math/Bayer.js';

// Generate 3D noise texture
function createNoiseTexture3D(size = 128) {
  const data = new Uint8Array(size * size * size);
  const perlin = new ImprovedNoise();
  let i = 0;

  for (let z = 0; z < size; z++) {
    for (let y = 0; y < size; y++) {
      for (let x = 0; x < size; x++) {
        const nx = (x / size) * 5;
        const ny = (y / size) * 5;
        const nz = (z / size) * 5;
        data[i] = 128 + 128 * perlin.noise(nx * 10, ny * 10, nz * 10);
        i++;
      }
    }
  }

  const texture = new THREE.Data3DTexture(data, size, size, size);
  texture.format = THREE.RedFormat;
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  texture.needsUpdate = true;
  return texture;
}

// Volumetric material
const noiseTexture = createNoiseTexture3D();
const smokeAmount = uniform(2);

const volumetricMaterial = new VolumeNodeMaterial();
volumetricMaterial.steps = 12;
volumetricMaterial.offsetNode = bayer16(screenCoordinate); // dithering

volumetricMaterial.scatteringNode = Fn(({ positionRay }) => {
  const timeScaled = vec3(time, 0, time.mul(0.3));

  const sampleGrain = (scale, timeScale = 1) =>
    texture3D(noiseTexture, positionRay.add(timeScaled.mul(timeScale)).mul(scale).mod(1), 0)
      .r.add(0.5);

  let density = sampleGrain(0.1);
  density = density.mul(sampleGrain(0.05, 1));
  density = density.mul(sampleGrain(0.02, 2));

  return smokeAmount.mix(1, density);
});

const volumetricMesh = new THREE.Mesh(
  new THREE.BoxGeometry(50, 40, 50),
  volumetricMaterial
);
volumetricMesh.receiveShadow = true;
scene.add(volumetricMesh);
```

### Reflector/Mirror Surface

```ts
import { Reflector } from 'three/addons/objects/Reflector.js';

const mirrorGeometry = new THREE.PlaneGeometry(10, 10);
const mirror = new Reflector(mirrorGeometry, {
  textureWidth: window.innerWidth * window.devicePixelRatio,
  textureHeight: window.innerHeight * window.devicePixelRatio,
  color: 0x889999,
});
mirror.position.y = 0.01;
mirror.rotation.x = -Math.PI / 2;
scene.add(mirror);
```

### Lensflare

```ts
import { Lensflare, LensflareElement } from 'three/addons/objects/Lensflare.js';

const light = new THREE.PointLight(0xffffff, 1.5, 2000);

const textureLoader = new THREE.TextureLoader();
const textureFlare0 = textureLoader.load('textures/lensflare/lensflare0.png');
const textureFlare1 = textureLoader.load('textures/lensflare/lensflare1.png');

const lensflare = new Lensflare();
lensflare.addElement(new LensflareElement(textureFlare0, 700, 0, light.color));
lensflare.addElement(new LensflareElement(textureFlare1, 300, 0.2));
lensflare.addElement(new LensflareElement(textureFlare1, 600, 0.6));
light.add(lensflare);
scene.add(light);
```

### CSS3D Renderer (HTML in 3D)

```ts
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';

const cssRenderer = new CSS3DRenderer();
cssRenderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(cssRenderer.domElement);

// Convert HTML element to 3D object
const div = document.createElement('div');
div.innerHTML = '<h1>Hello 3D HTML</h1>';
div.style.backgroundColor = 'rgba(0,0,0,0.5)';

const cssObject = new CSS3DObject(div);
cssObject.position.set(0, 0, 200);
scene.add(cssObject);
```

### Marching Cubes (Metaballs)

```ts
import { MarchingCubes } from 'three/addons/objects/MarchingCubes.js';

const resolution = 28;
const marchingCubes = new MarchingCubes(resolution, material, true, true);
marchingCubes.isolation = 0.5;

// Update metaballs each frame
function updateMetaballs(time) {
  marchingCubes.reset();

  // Add balls
  const strength = 0.5;
  const subtract = 12;

  for (let i = 0; i < numBalls; i++) {
    const ballx = Math.sin(i + 1.26 * time * (1.03 + 0.5 * Math.cos(0.21 * i))) * 0.27 + 0.5;
    const bally = Math.abs(Math.cos(i + 1.12 * time * Math.cos(1.22 + 0.1424 * i))) * 0.77;
    const ballz = Math.cos(i + 1.32 * time * 0.1 * Math.sin(0.92 + 0.53 * i)) * 0.27 + 0.5;

    marchingCubes.addBall(ballx, bally, ballz, strength, subtract);
  }
}
```

## Advanced Post-Processing (Native Three.js)

### EffectComposer Pipeline

```ts
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const composer = new EffectComposer(renderer);

// Render pass
const renderPass = new RenderPass(scene, camera);
composer.addPass(renderPass);

// Unreal Bloom
const bloomPass = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight),
  1.5,  // strength
  0.4,  // radius
  0.85  // threshold
);
composer.addPass(bloomPass);

// Output
const outputPass = new OutputPass();
composer.addPass(outputPass);

// Render
function animate() {
  composer.render();
}
```

### Selective Bloom (Objects with bloom layer)

```ts
const BLOOM_LAYER = 1;
const bloomLayer = new THREE.Layers();
bloomLayer.set(BLOOM_LAYER);

const darkMaterial = new THREE.MeshBasicMaterial({ color: 'black' });
const materials = {};

// Make specific objects bloom
bloomObject.layers.enable(BLOOM_LAYER);

// In render: render bloom scene separately, then composite
function renderBloom() {
  // Replace non-bloom objects with dark material
  scene.traverse((obj) => {
    if (obj.isMesh && !bloomLayer.test(obj.layers)) {
      materials[obj.uuid] = obj.material;
      obj.material = darkMaterial;
    }
  });

  bloomComposer.render();

  // Restore materials
  scene.traverse((obj) => {
    if (materials[obj.uuid]) {
      obj.material = materials[obj.uuid];
      delete materials[obj.uuid];
    }
  });
}
```

### WebGPU Post-Processing with TSL

```ts
import * as THREE from 'three/webgpu';
import { pass, mrt, output, emissive } from 'three/tsl';
import { bloom } from 'three/addons/tsl/display/BloomNode.js';
import { lensflare } from 'three/addons/tsl/display/LensflareNode.js';
import { gaussianBlur } from 'three/addons/tsl/display/GaussianBlurNode.js';

// Scene pass with MRT
const scenePass = pass(scene, camera);
scenePass.setMRT(mrt({ output, emissive }));

// Get textures
const outputPass = scenePass.getTextureNode();
const emissivePass = scenePass.getTextureNode('emissive');

// Bloom from emissive
const bloomPass = bloom(emissivePass, 1, 1);

// Lensflare
const flarePass = lensflare(bloomPass, {
  threshold: uniform(0.5),
  ghostAttenuationFactor: uniform(25),
  ghostSpacing: uniform(0.25),
});

// Optional blur
const blurPass = gaussianBlur(flarePass, 8);

// Composite
const renderPipeline = new THREE.RenderPipeline(renderer);
renderPipeline.outputNode = outputPass.add(bloomPass).add(blurPass);

// Render
function animate() {
  renderPipeline.render();
}
```

### God Rays

```ts
import { GodRaysPass } from 'three/addons/postprocessing/GodRaysPass.js';

// Create sun mesh
const sunGeometry = new THREE.SphereGeometry(5, 32, 32);
const sunMaterial = new THREE.MeshBasicMaterial({ color: 0xffdd00 });
const sun = new THREE.Mesh(sunGeometry, sunMaterial);
scene.add(sun);

const godRaysPass = new GodRaysPass(scene, camera, sun, {
  resolutionScale: 0.5,
  density: 0.96,
  decay: 0.93,
  weight: 0.4,
  exposure: 0.6,
  samples: 60,
});

composer.addPass(godRaysPass);
```

### Film Grain & Color Grading

```ts
import { FilmPass } from 'three/addons/postprocessing/FilmPass.js';
import { ColorCorrectionShader } from 'three/addons/shaders/ColorCorrectionShader.js';
import { HueSaturationShader } from 'three/addons/shaders/HueSaturationShader.js';

// Film grain
const filmPass = new FilmPass(0.35, 0.025, 648, false);
composer.addPass(filmPass);

// Color correction
const colorCorrectionPass = new ShaderPass(ColorCorrectionShader);
colorCorrectionPass.uniforms['powRGB'].value = new THREE.Vector3(1.2, 1.1, 1.0);
composer.addPass(colorCorrectionPass);

// Hue/Saturation
const hueSatPass = new ShaderPass(HueSaturationShader);
hueSatPass.uniforms['hue'].value = 0;
hueSatPass.uniforms['saturation'].value = 0.2;
composer.addPass(hueSatPass);
```

### Custom Post-Processing Shader Pass

```ts
const customShader = {
  uniforms: {
    tDiffuse: { value: null },
    uTime: { value: 0 },
    uIntensity: { value: 0.5 },
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    uniform float uTime;
    uniform float uIntensity;
    varying vec2 vUv;

    void main() {
      vec2 uv = vUv;

      // Chromatic aberration offset
      float offset = uIntensity * 0.01;
      float r = texture2D(tDiffuse, uv + vec2(offset, 0.0)).r;
      float g = texture2D(tDiffuse, uv).g;
      float b = texture2D(tDiffuse, uv - vec2(offset, 0.0)).b;

      gl_FragColor = vec4(r, g, b, 1.0);
    }
  `,
};

const customPass = new ShaderPass(customShader);
composer.addPass(customPass);

// Update uniform in animation loop
customPass.uniforms['uTime'].value = clock.getElapsedTime();
```

## Performance Optimization Advanced

### Level of Detail (LOD)

```ts
const lod = new THREE.LOD();

// Detail levels
const highDetail = new THREE.Mesh(highGeo, material);   // 0-10 units
const medDetail = new THREE.Mesh(medGeo, material);     // 10-50 units
const lowDetail = new THREE.Mesh(lowGeo, material);     // 50-200 units

lod.addLevel(highDetail, 0);
lod.addLevel(medDetail, 10);
lod.addLevel(lowDetail, 50);

scene.add(lod);
```

### Frustum Culling (Automatic)

```ts
// Three.js does this automatically, but you can control it:
mesh.frustumCulled = true; // default

// For objects that should always render:
skybox.frustumCulled = false;
```

### GPU Picking (WebGPU Compute)

```ts
// Use compute shader for raycasting on GPU
const pickBuffer = storage(new THREE.StorageBufferAttribute(1, 'vec4'));

const computePick = Fn(() => {
  // GPU-accelerated intersection test
  // Returns picked object ID
});

renderer.compute(computePick().compute(1));
```

### Texture Compression (KTX2/Basis)

```ts
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const ktx2Loader = new KTX2Loader()
  .setTranscoderPath('/basis/')
  .detectSupport(renderer);

ktx2Loader.load('/textures/compressed.ktx2', (texture) => {
  texture.encoding = THREE.sRGBEncoding;
  material.map = texture;
  material.needsUpdate = true;
});
```

### BatchedMesh (Reduces Draw Calls)

```ts
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshStandardMaterial();

const batchedMesh = new THREE.BatchMesh(1000, geometry, material);

// Add instances at runtime
for (let i = 0; i < 1000; i++) {
  const id = batchedMesh.addInstance(geometry);
  batchedMesh.setMatrixAt(id, matrix);
  batchedMesh.setColorAt(id, color);
}

scene.add(batchedMesh);
```

### WebXR Performance Tips

```ts
// Use foveated rendering (reduces peripheral resolution)
renderer.xr.setFoveation(0.5); // 0 = none, 1 = max

// Reference space type affects performance
renderer.xr.setReferenceSpaceType('local-floor');

// Frame rate
session.requestAnimationFrame((time, frame) => {
  // Render at XR frame rate (usually 72-120Hz)
});
```

## Famous Three.js Examples & Inspiration

### Official Examples to Study

| Example | Technique |
|---------|-----------|
| `webgl_animation_keyframes` | GLTF skeletal animation |
| `webgl_animation_skinning_morph` | Morph targets + skeleton |
| `webgl_effects_anaglyph` | Stereo 3D effect |
| `webgl_geometry_terrain` | Procedural terrain |
| `webgl_interactive_voxelpainter` | Voxel building |
| `webgl_lightprobe` | Light probes |
| `webgl_loader_gltf` | GLTF model loading |
| `webgl_materials_envmaps` | Environment mapping |
| `webgl_materials_physical_clearcoat` | Car paint material |
| `webgl_mirror` | Mirror reflection |
| `webgl_modifier_subdivision` | Mesh subdivision |
| `webgl_multiple_views` | Multi-viewport |
| `webgl_panorama_equirectangular` | 360° panorama |
| `webgl_postprocessing_unreal_bloom` | Bloom effect |
| `webgl_raycaster_bvh` | Fast raycasting |
| `webgl_shaders_ocean` | Ocean shader |
| `webgl_shadowmap_pcss` | Soft shadows |
| `webgpu_compute_particles` | GPU particles |
| `webgpu_materials` | TSL materials |
| `webgpu_postprocessing` | WebGPU effects |
| `webxr_vr_handinput` | VR hand tracking |

### Awwwards-Worthy Techniques

1. **Scroll-driven storytelling**: GSAP ScrollTrigger + camera paths
2. **Liquid/morphing shapes**: Custom vertex shaders + noise
3. **Parallax layers**: Multiple render passes at different depths
4. **Cursor-reactive geometry**: Raycasting + vertex displacement
5. **Page transitions**: 3D object morphing between scenes
6. **Loading sequences**: Animated progress with 3D elements
7. **Grain/noise overlays**: Film grain post-processing
8. **Smooth locomotion**: Lenis + camera interpolation

### Creative Coding Resources

| Site | Description |
|------|-------------|
| [threejs.org/examples](https://threejs.org/examples) | Official examples (500+) |
| [threejs-journey.com](https://threejs-journey.com) | Best course (Bruno Simon) |
| [shadertoy.com](https://shadertoy.com) | GLSL shader playground |
| [glslsandbox.com](https://glslsandbox.com) | Fragment shader experiments |
| [thebookofshaders.com](https://thebookofshaders.com) | Shader fundamentals |
| [awwwards.com/3d](https://www.awwwards.com/3d/) | Awwwards 3D showcase |
| [codrops.com](https://tympanus.net/codrops/) | Creative tutorials |
| [made-with-threejs.com](https://made-with-threejs.com) | Community gallery |
| [three-bunches.io](https://three-bunches.io) | Curated examples |
| [github.com/mrdoob/three.js](https://github.com/mrdoob/three.js/tree/dev/examples) | Source examples |

## References

- [R3F Documentation](https://r3f.docs.pmnd.rs)
- [Drei Documentation](https://drei.docs.pmnd.rs)
- [Three.js Documentation](https://threejs.org/docs)
- [Three.js Manual](https://threejs.org/manual)
- [Three.js Examples](https://threejs.org/examples)
- [Three.js GitHub](https://github.com/mrdoob/three.js)
- [Three.js Journey](https://threejs-journey.com)
- [TSL Documentation (Node Materials)](https://github.com/mrdoob/three.js/blob/dev/docs/llms.txt)
- [WebGPU in Three.js](https://threejs.org/docs/#api/en/renderers/WebGPURenderer)
- [GLSL Sandbox](https://glslsandbox.com)
- [Shadertoy](https://www.shadertoy.com)
- [The Book of Shaders](https://thebookofshaders.com)
- [Awwwards 3D Sites](https://www.awwwards.com/3d/)
- [Codrops](https://tympanus.net/codrops/)
- [Made with Three.js](https://made-with-threejs.com)
- [Rapier Physics](https://rapier.rs)
- [Cannon.js Physics](https://github.com/pmndrs/cannon-es)
- [WebXR Device API](https://developer.mozilla.org/en-US/docs/Web/API/WebXR_Device_API)
