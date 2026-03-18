# gamecore.cpp — CCharacterCore traduit ligne par ligne
# Tick() + TickDeferred() + VelocityRamp()

import math
import collision
from tuning import *


def velocity_ramp(value):
    """gamecore.cpp:122 VelocityRamp() — identique"""
    if value < VELRAMP_START:
        return 1.0
    return 1.0 / (VELRAMP_CURVATURE ** ((value - VELRAMP_START) / VELRAMP_RANGE))


class CCharacterCore:
    """
    Traduction exacte de CCharacterCore.
    Noms de variables identiques au source C++ (sans m_ prefix).
    """

    def reset(self, spawn_x, spawn_y):
        self.pos_x      = float(spawn_x)
        self.pos_y      = float(spawn_y)
        self.vel_x      = 0.0
        self.vel_y      = 0.0

        # hook
        self.hook_state  = HOOK_IDLE
        self.hook_pos_x  = 0.0
        self.hook_pos_y  = 0.0
        self.hook_dir_x  = 0.0
        self.hook_dir_y  = 0.0
        self.hook_tick   = 0

        # jump
        self.jumped      = 0   # bitmask
        self.jumped_total= 0
        self.jumps       = 2   # m_Jumps = 2 par défaut

        self.direction   = 0
        self.angle       = 0   # en unités DDNet (radians * 256)

    def tick(self, inp_direction, inp_jump, inp_hook, target_x, target_y):
        """
        CCharacterCore::Tick() — traduction exacte.

        inp_direction : -1, 0, 1
        inp_jump      : bool
        inp_hook      : bool
        target_x/y    : direction de visée normalisée (vers la souris)
        """

        # get ground state
        grounded = collision.is_on_ground(self.pos_x, self.pos_y)

        # normalize target direction (comme DDNet : normalize(vec2(TargetX, TargetY)))
        tlen = math.hypot(target_x, target_y)
        if tlen > 0:
            tdir_x = target_x / tlen
            tdir_y = target_y / tlen
        else:
            tdir_x, tdir_y = 0.0, -1.0

        # vel.y += gravity
        self.vel_y += GRAVITY

        # MaxSpeed / Accel / Friction
        if grounded:
            max_speed = GROUND_CONTROL_SPEED
            accel     = GROUND_CONTROL_ACCEL
            friction  = GROUND_FRICTION
        else:
            max_speed = AIR_CONTROL_SPEED
            accel     = AIR_CONTROL_ACCEL
            friction  = AIR_FRICTION

        self.direction = inp_direction

        # handle jump — bitmask identique à gamecore.cpp:227
        if inp_jump:
            if not (self.jumped & 1):
                if grounded and (not (self.jumped & 2) or self.jumps != 0):
                    # ground jump
                    self.vel_y       = -GROUND_JUMP_IMPULSE
                    self.jumped     |= (1 if self.jumps > 1 else 3)
                    self.jumped_total = 0
                elif not (self.jumped & 2):
                    # air jump
                    self.vel_y       = -AIR_JUMP_IMPULSE
                    self.jumped     |= 3
                    self.jumped_total += 1
        else:
            self.jumped &= ~1  # relâche bit 0

        # handle hook — lancer (gamecore.cpp:260)
        if inp_hook:
            if self.hook_state == HOOK_IDLE:
                self.hook_state  = HOOK_FLYING
                self.hook_pos_x  = self.pos_x + tdir_x * PHYS_SIZE * 1.5
                self.hook_pos_y  = self.pos_y + tdir_y * PHYS_SIZE * 1.5
                self.hook_dir_x  = tdir_x
                self.hook_dir_y  = tdir_y
                self.hook_tick   = float(SERVER_TICK_SPEED)
        else:
            # relâche le grappin
            self.hook_state = HOOK_IDLE
            self.hook_pos_x = self.pos_x
            self.hook_pos_y = self.pos_y

        # hook flying — avance la tête du grappin (gamecore.cpp:285+)
        if self.hook_state == HOOK_FLYING:
            new_hx = self.hook_pos_x + self.hook_dir_x * HOOK_FIRE_SPEED
            new_hy = self.hook_pos_y + self.hook_dir_y * HOOK_FIRE_SPEED
            # distance max dépassée ?
            dist = math.hypot(new_hx - self.pos_x, new_hy - self.pos_y)
            if dist > HOOK_LENGTH:
                self.hook_state = HOOK_IDLE
                self.hook_pos_x = self.pos_x
                self.hook_pos_y = self.pos_y
            else:
                hit = collision.intersect_line(
                    self.hook_pos_x, self.hook_pos_y, new_hx, new_hy
                )
                if hit:
                    self.hook_pos_x = hit[0]
                    self.hook_pos_y = hit[1]
                    self.hook_state = HOOK_GRABBED
                else:
                    self.hook_pos_x = new_hx
                    self.hook_pos_y = new_hy

        # mouvement horizontal — vel.x = clamp(vel.x*friction + dir*accel, -max, max)
        self.vel_x *= friction
        if self.direction != 0:
            self.vel_x += self.direction * accel
            if self.vel_x > max_speed:  self.vel_x =  max_speed
            if self.vel_x < -max_speed: self.vel_x = -max_speed

        # Move — VelocityRamp + MoveBox (gamecore.cpp:Move)
        speed = math.hypot(self.vel_x, self.vel_y)
        ramp  = velocity_ramp(speed)
        new_px, new_py, new_vx, new_vy, landed = collision.move_box(
            self.pos_x, self.pos_y,
            self.vel_x * ramp,
            self.vel_y * ramp,
        )
        self.pos_x = new_px
        self.pos_y = new_py
        # On conserve vel sans ramp pour le prochain tick
        if speed * ramp > 0:
            ratio = math.hypot(new_vx, new_vy) / (speed * ramp + 1e-9)
            self.vel_x = new_vx / ramp if ramp > 0 else 0.0
            self.vel_y = new_vy / ramp if ramp > 0 else 0.0
        else:
            self.vel_x = new_vx
            self.vel_y = new_vy

        # reset jumped au sol
        if landed or grounded:
            self.jumped &= ~2

    def tick_deferred(self):
        """
        CCharacterCore::TickDeferred() — force du grappin accroché.
        Appelé après tick().
        """
        if self.hook_state != HOOK_GRABBED:
            return

        dx   = self.hook_pos_x - self.pos_x
        dy   = self.hook_pos_y - self.pos_y
        dist = math.hypot(dx, dy)
        if dist < 1.0:
            return

        nx = dx / dist
        ny = dy / dist

        # contrainte de pendule : annule la composante qui s'éloigne
        dot = self.vel_x * nx + self.vel_y * ny
        if dot < 0:
            self.vel_x -= dot * nx
            self.vel_y -= dot * ny

        # force d'attraction
        self.vel_x += nx * HOOK_DRAG_ACCEL
        self.vel_y += ny * HOOK_DRAG_ACCEL

        # plafonner à hook_drag_speed
        speed = math.hypot(self.vel_x, self.vel_y)
        if speed > HOOK_DRAG_SPEED:
            self.vel_x = self.vel_x / speed * HOOK_DRAG_SPEED
            self.vel_y = self.vel_y / speed * HOOK_DRAG_SPEED

    @property
    def jumps_left(self):
        return 0 if (self.jumped & 2) else (2 if self.jumps >= 2 else 1)