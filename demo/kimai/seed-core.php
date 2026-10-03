<?php

/*
 * Kimai core data of the Studio Weber demo world: users, teams, customers,
 * projects, activities, rates and timesheets (partly exported, two running).
 * The plugins add their own data afterwards (<Bundle>/demo/seed.php).
 *
 * Run inside the Kimai container (demo/kimai/reset.sh does it):
 *   DEMO_LANG=de php /opt/demo/kimai/seed-core.php
 */

use App\Entity\Activity;
use App\Entity\Customer;
use App\Entity\Project;
use App\Entity\ProjectRate;
use App\Entity\Team;
use App\Entity\Timesheet;
use App\Entity\User;
use App\Entity\UserPreference;
use App\Kernel;

const KIMAI_ROOT = '/opt/kimai';

require KIMAI_ROOT . '/vendor/autoload.php';
require __DIR__ . '/../dist/DemoWorld.php';
(new Symfony\Component\Dotenv\Dotenv())->bootEnv(KIMAI_ROOT . '/.env');

$kernel = new Kernel('prod', false);
$kernel->boot();
$em = $kernel->getContainer()->get('doctrine')->getManager();

$lang = getenv('DEMO_LANG') ?: 'de';
// Kimai runs on the real clock: place the data around the real today.
$world = new DemoWorld($lang, __DIR__ . '/../dist/world.json', 'today');
$w = $world->data;
$zone = new DateTimeZone($w['timezone']);

if ($em->getRepository(Customer::class)->findOneBy(['name' => $w['customers'][0]['name']]) !== null) {
    echo "Already seeded.\n";
    exit(0);
}

$pref = static function (User $user, string $name, string $value) use ($em): void {
    $preference = $user->getPreference($name);
    if ($preference === null) {
        $preference = new UserPreference($name, $value);
        $user->addPreference($preference);
    }
    $preference->setValue($value);
    $em->persist($preference);
};

// --- Users: the image created Mara (ADMINMAIL) as "admin"; the others share her password hash.
$userRepo = $em->getRepository(User::class);
$owner = $w['people'][0];      // Mara, the studio's owner
$mara = $userRepo->findOneBy(['email' => $owner['email']]);
$users = [];
foreach ($w['people'] as $person) {
    $user = $person['id'] === $owner['id'] ? $mara : new User();
    $user->setUserIdentifier($person['id']);
    $user->setEmail($person['email']);
    $user->setAlias($person['name']);
    $user->setTitle($world->t($person['title']));
    $user->setColor($person['color']);
    $user->setEnabled(true);
    if ($person['id'] !== $owner['id']) {
        $user->setPassword($mara->getPassword());
        $user->setRoles([$person['kimai_role']]);
    }
    $user->setWorkStartingDay(new DateTime($person['since'], $zone));
    $perDay = (int) round($person['hours_per_week'] / 5 * 3600);
    foreach (['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] as $day) {
        $user->{"setWorkHours$day"}($perDay);
    }
    $user->setHolidaysPerYear($person['holidays_per_year']);
    $user->setWorkContractMode('day');
    $em->persist($user);
    $pref($user, '__wizards__', 'intro,profile');
    $pref($user, 'language', $lang);
    $pref($user, 'locale', $lang);
    $pref($user, 'timezone', $w['timezone']);
    $pref($user, 'hourly_rate', (string) $person['hourly_rate']);
    $users[$person['id']] = $user;
}

foreach ($w['teams'] as $t) {
    $team = new Team($world->t($t['name']));
    foreach ($t['members'] as $id) {
        $id === $t['lead'] ? $team->addTeamlead($users[$id]) : $team->addUser($users[$id]);
    }
    if (!in_array($t['lead'], $t['members'], true)) {
        $team->addTeamlead($users[$t['lead']]);
    }
    $em->persist($team);
}

// --- Customers, projects, activities (colors from the Kante palette)
$customers = [];
foreach ($w['customers'] as $c) {
    $customer = new Customer($c['name']);
    $customer->setColor($c['color']);
    $customer->setCountry($c['country']);
    $customer->setCurrency($w['currency']);
    $customer->setTimezone($w['timezone']);
    $customer->setCity($c['city']);
    $customer->setVatId($c['vat_id'] ?: null);
    $customer->setComment($world->t($c['kind']));
    $customer->setBillable($c['id'] !== 'studio');
    $em->persist($customer);
    $customers[$c['id']] = $customer;
}

$projects = [];
foreach ($w['projects'] as $p) {
    $project = new Project();
    $project->setName($world->t($p['name']));
    $project->setCustomer($customers[$p['customer']]);
    $project->setColor($p['color']);
    $project->setBillable($p['billable']);
    $em->persist($project);
    if ($p['hourly_rate'] > 0) {
        $rate = new ProjectRate();
        $rate->setProject($project);
        $rate->setRate($p['hourly_rate']);
        $em->persist($rate);
    }
    $projects[$p['id']] = $project;
}

$activities = [];
foreach ($w['activities'] as $a) {
    $activity = new Activity();
    $activity->setName($world->t($a['name']));
    $activity->setColor($a['color']);
    $em->persist($activity);
    $activities[$a['id']] = $activity;
}
$em->flush();

// --- Timesheets
$rates = array_column($w['projects'], null, 'id');
$sheet = static function (array $row, DateTime $begin, ?DateTime $end) use ($users, $projects, $activities, $rates, $world, $em): Timesheet {
    $ts = new Timesheet();
    $ts->setUser($users[$row['user']]);
    $ts->setProject($projects[$row['project']]);
    $ts->setActivity($activities[$row['activity']]);
    $ts->setBegin($begin);
    $ts->setDescription($world->t($row['description']));
    $ts->setTimezone($begin->getTimezone()->getName());
    $billable = $rates[$row['project']]['billable'];
    $ts->setBillable($billable);
    $hourly = (float) $rates[$row['project']]['hourly_rate'];
    $ts->setHourlyRate($hourly);
    if ($end !== null) {
        $ts->setEnd($end);
        $seconds = $end->getTimestamp() - $begin->getTimestamp();
        $ts->setDuration($seconds);
        $ts->setRate(round($hourly * $seconds / 3600, 2));
        $ts->setExported($row['exported'] ?? false);
    }
    $em->persist($ts);
    return $ts;
};

$now = new DateTimeImmutable('now', $zone);
$count = 0;
foreach ($world->pastTimesheets($now) as $row) {
    $begin = DateTime::createFromImmutable($world->date($row['day'], $row['start']));
    $end = DateTime::createFromImmutable($world->date($row['day'], $row['end']));
    $sheet($row, $begin, $end);
    $count++;
}
foreach ($w['running'] as $row) {
    $start = $world->date($world->todayOffset, $row['start']);
    if ($start > $now) {
        $start = $now->modify('-47 minutes');
    }
    $sheet($row, DateTime::createFromImmutable($start), null);
}
$em->flush();

echo "Seeded Studio Weber: " . count($users) . " users, $count timesheets, " . count($w['running']) . " running ($lang).\n";
